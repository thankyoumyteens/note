# 实现 streamChat

打开你的：

```text
client.openai/OpenAiCompatibleLlmClient.java
```

增加几个 import：

```java
import com.example.aigateway.client.openai.dto.ChatCompletionChunk;
import com.fasterxml.jackson.databind.ObjectMapper;
import reactor.core.publisher.Flux;
```

然后给类增加一个 `ObjectMapper` 字段。

完整版本如下：

```java
package com.example.aigateway.client.openai;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.client.openai.dto.ChatCompletionChunk;
import com.example.aigateway.client.openai.dto.ChatCompletionRequest;
import com.example.aigateway.client.openai.dto.ChatCompletionResponse;
import com.example.aigateway.config.LlmProperties;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.List;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import reactor.core.publisher.Flux;

@Component
public class OpenAiCompatibleLlmClient implements LlmClient {

    private final WebClient llmWebClient;
    private final LlmProperties properties;
    private final ObjectMapper objectMapper;

    public OpenAiCompatibleLlmClient(
            WebClient llmWebClient,
            LlmProperties properties,
            ObjectMapper objectMapper
    ) {
        this.llmWebClient = llmWebClient;
        this.properties = properties;
        this.objectMapper = objectMapper;
    }

    @Override
    public String chat(String message) {
        ChatCompletionRequest request = buildRequest(message, false);

        try {
            ChatCompletionResponse response = llmWebClient.post()
                    .uri("/v1/chat/completions")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(ChatCompletionResponse.class)
                    .block();

            if (response == null || response.choices() == null || response.choices().isEmpty()) {
                throw new IllegalStateException("LLM response is empty");
            }

            ChatCompletionResponse.Choice firstChoice = response.choices().get(0);

            if (firstChoice.message() == null || firstChoice.message().content() == null) {
                throw new IllegalStateException("LLM response message is empty");
            }

            return firstChoice.message().content().strip();

        } catch (WebClientResponseException e) {
            throw new RuntimeException(
                    "LLM API error. status=" + e.getStatusCode() +
                            ", body=" + e.getResponseBodyAsString(),
                    e
            );
        } catch (Exception e) {
            throw new RuntimeException("Failed to call LLM API: " + e.getMessage(), e);
        }
    }

    @Override
    public Flux<String> streamChat(String message) {
        ChatCompletionRequest request = buildRequest(message, true);

        return llmWebClient.post()
                .uri("/v1/chat/completions")
                .bodyValue(request)
                .retrieve()
                .bodyToFlux(String.class)
                .flatMap(this::parseSseChunk)
                .onErrorResume(e -> Flux.just("[ERROR] " + e.getMessage()));
    }

    private ChatCompletionRequest buildRequest(String message, boolean stream) {
        return new ChatCompletionRequest(
                properties.getModel(),
                List.of(
                        new ChatCompletionRequest.Message(
                                "system",
                                "你是一个严谨、简洁的 AI 应用开发助手。"
                        ),
                        new ChatCompletionRequest.Message(
                                "user",
                                message
                        )
                ),
                0.3,
                stream
        );
    }

    private Flux<String> parseSseChunk(String rawChunk) {
        if (rawChunk == null || rawChunk.isBlank()) {
            return Flux.empty();
        }

        String chunk = rawChunk.strip();

        if (chunk.equals("[DONE]") || chunk.equals("data: [DONE]")) {
            return Flux.empty();
        }

        if (chunk.startsWith("data:")) {
            chunk = chunk.substring("data:".length()).strip();
        }

        if (chunk.isBlank() || chunk.equals("[DONE]")) {
            return Flux.empty();
        }

        try {
            ChatCompletionChunk parsed = objectMapper.readValue(chunk, ChatCompletionChunk.class);

            if (parsed.choices() == null || parsed.choices().isEmpty()) {
                return Flux.empty();
            }

            ChatCompletionChunk.Choice choice = parsed.choices().get(0);

            if (choice.delta() == null || choice.delta().content() == null) {
                return Flux.empty();
            }

            return Flux.just(choice.delta().content());

        } catch (Exception e) {
            return Flux.empty();
        }
    }
}
```

## 一个重要说明：bodyToFlux(String.class) 的兼容问题

不同供应商对 SSE 的返回格式略有差异。

有的 `bodyToFlux(String.class)` 得到的是：

```text
{"choices":[{"delta":{"content":"RAG"}}]}
```

有的得到的是：

```text
data: {"choices":[{"delta":{"content":"RAG"}}]}
```

所以我在 `parseSseChunk` 里兼容了：

```java
if (chunk.startsWith("data:")) {
    chunk = chunk.substring("data:".length()).strip();
}
```

如果你的供应商返回格式更特殊，可以自行根据你的实际返回调整。
