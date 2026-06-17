# Anthropic Messages Stream Client

Anthropic-compatible SSE 是命名事件，主要关心：

```text
event: content_block_delta
data: {"delta":{"type":"text_delta","text":"..."}}
```

所以要读取 `ServerSentEvent.event()` 和 `ServerSentEvent.data()`。

```java
package com.example.ai.client;

import com.example.ai.config.AiProviderProperties;
import com.example.ai.dto.LlmMessage;
import com.example.ai.dto.StreamChatRequest;
import com.example.ai.dto.anthropic.AnthropicMessageStreamRequest;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;

import java.util.List;

/**
 * Anthropic Messages-compatible streaming client。
 * 支持 Claude 原生 Messages API 和 Qwen Anthropic-compatible Messages API。
 */
@Component
public class AnthropicMessagesStreamClient implements ProviderStreamClient {

    private static final ParameterizedTypeReference<ServerSentEvent<String>> SSE_STRING =
            new ParameterizedTypeReference<>() {
            };

    private final WebClient.Builder webClientBuilder;
    private final ObjectMapper objectMapper;

    public AnthropicMessagesStreamClient(WebClient.Builder webClientBuilder,
                                         ObjectMapper objectMapper) {
        this.webClientBuilder = webClientBuilder;
        this.objectMapper = objectMapper;
    }

    @Override
    public boolean supports(AiProviderProperties.ProviderType type) {
        return type == AiProviderProperties.ProviderType.ANTHROPIC_MESSAGES;
    }

    @Override
    public Flux<String> stream(AiProviderProperties.ProviderConfig config,
                               StreamChatRequest request) {
        WebClient webClient = webClientBuilder
                .baseUrl(config.baseUrl())
                .defaultHeader("x-api-key", config.apiKey())
                .defaultHeader("anthropic-version", "2023-06-01")
                .build();

        AnthropicMessageStreamRequest body = new AnthropicMessageStreamRequest(
                config.model(),
                config.maxTokens(),
                config.temperature(),
                request.system(),
                List.of(new LlmMessage("user", request.message())),
                true,
                shouldDisableThinking(config)
                        ? AnthropicMessageStreamRequest.disabledThinking()
                        : null
        );

        return webClient.post()
                .uri(config.path())
                .bodyValue(body)
                .retrieve()
                .onStatus(
                        HttpStatusCode::isError,
                        response -> response.bodyToMono(String.class)
                                .map(errorBody -> new RuntimeException(
                                        "Anthropic-compatible streaming error, status="
                                                + response.statusCode()
                                                + ", body="
                                                + errorBody
                                ))
                )
                .bodyToFlux(SSE_STRING)
                .takeUntil(event -> "message_stop".equals(event.event()))
                .filter(event -> "content_block_delta".equals(event.event()))
                .map(ServerSentEvent::data)
                .filter(data -> data != null && !data.isBlank())
                .map(this::extractAnthropicTextDelta)
                .filter(chunk -> !chunk.isBlank());
    }

    private boolean shouldDisableThinking(AiProviderProperties.ProviderConfig config) {
        return Boolean.TRUE.equals(config.thinkingDisabled());
    }

    private String extractAnthropicTextDelta(String data) {
        try {
            JsonNode root = objectMapper.readTree(data);
            JsonNode delta = root.path("delta");

            if (!"text_delta".equals(delta.path("type").asText())) {
                return "";
            }

            return delta.path("text").asText("");
        } catch (Exception e) {
            return "";
        }
    }
}
```
