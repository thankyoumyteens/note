# AnthropicProviderClient

## AnthropicChatRequest

```java
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * Anthropic Messages API 请求体。
 * system 是顶层字段，messages 只放 user / assistant。
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record AnthropicChatRequest(
        String model,

        @JsonProperty("max_tokens")
        Integer maxTokens,

        Double temperature,

        @JsonProperty("top_p")
        Double topP,

        String system,

        List<Message> messages
) {

    /**
     * Anthropic message。
     * role 只能是 user 或 assistant。
     */
    public record Message(
            String role,
            String content
    ) {
    }
}
```

## AnthropicChatResponse

```java
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * Anthropic Messages API 响应体。
 * content 是数组，文本结果通常在 type=text 的 content block 里。
 */
public record AnthropicChatResponse(
        String id,
        String type,
        String role,
        String model,
        List<ContentBlock> content,

        @JsonProperty("stop_reason")
        String stopReason,

        @JsonProperty("stop_sequence")
        String stopSequence,

        Usage usage
) {

    /**
     * 获取第一个文本 block 的内容。
     * 没有文本时返回空字符串，保证调用方拿到稳定 String。
     */
    public String firstText() {
        if (content == null || content.isEmpty()) {
            return "";
        }

        return content.stream()
                .filter(block -> "text".equals(block.type()))
                .map(ContentBlock::text)
                .filter(text -> text != null && !text.isBlank())
                .findFirst()
                .orElse("");
    }

    /**
     * Anthropic content block。
     * 普通文本回答通常是 type=text。
     */
    public record ContentBlock(
            String type,
            String text
    ) {
    }

    /**
     * Anthropic token usage。
     */
    public record Usage(
            @JsonProperty("input_tokens")
            Integer inputTokens,

            @JsonProperty("output_tokens")
            Integer outputTokens
    ) {
    }
}
```

## AnthropicProviderClient

```java
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientRequestException;
import reactor.core.Exceptions;
import reactor.core.publisher.Mono;
import reactor.util.retry.Retry;

import java.time.Duration;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeoutException;

/**
 * Anthropic Messages API provider client。
 * 负责 Anthropic 协议转换、HTTP 错误处理、timeout 和 retry。
 */
public class AnthropicProviderClient implements LlmProviderClient {

    private final String provider;
    private final String apiKey;
    private final String model;
    private final String anthropicVersion;
    private final int requestTimeoutSeconds;
    private final int maxRetries;
    private final WebClient webClient;

    public AnthropicProviderClient(
            String provider,
            String baseUrl,
            String apiKey,
            String model,
            String anthropicVersion,
            int requestTimeoutSeconds,
            int maxRetries,
            int connectTimeoutMillis,
            int responseTimeoutSeconds
    ) {
        this.provider = provider;
        this.apiKey = apiKey;
        this.model = model;
        this.anthropicVersion = anthropicVersion;
        this.requestTimeoutSeconds = requestTimeoutSeconds;
        this.maxRetries = maxRetries;
        this.webClient = WebClientFactory.create(
                baseUrl,
                connectTimeoutMillis,
                responseTimeoutSeconds
        );
    }

    @Override
    public String provider() {
        return provider;
    }

    @Override
    public Mono<UnifiedChatResponse> chat(UnifiedChatRequest request) {
        AnthropicChatRequest providerRequest = toAnthropicRequest(request);

        return webClient.post()
                .uri("/messages")
                .header("x-api-key", apiKey)
                .header("anthropic-version", anthropicVersion)
                .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .bodyValue(providerRequest)
                .retrieve()
                .onStatus(
                        HttpStatusCode::isError,
                        response -> toException(response, "Provider server error")
                )
                .bodyToMono(AnthropicChatResponse.class)
                .timeout(Duration.ofSeconds(requestTimeoutSeconds))
                .retryWhen(
                        Retry.backoff(maxRetries, Duration.ofMillis(500))
                                .maxBackoff(Duration.ofSeconds(3))
                                .jitter(0.2)
                                .filter(this::isRetryable)
                                .onRetryExhaustedThrow((spec, signal) -> signal.failure())
                )
                .map(this::toUnifiedResponse);
    }

    private AnthropicChatRequest toAnthropicRequest(UnifiedChatRequest request) {
        List<AnthropicChatRequest.Message> messages = request.messages()
                .stream()
                .map(this::toAnthropicMessage)
                .toList();

        return new AnthropicChatRequest(
                model,
                request.options().maxTokens(),
                request.options().temperature(),
                request.options().topP(),
                request.system(),
                messages
        );
    }

    private AnthropicChatRequest.Message toAnthropicMessage(UnifiedChatMessage message) {
        String role = switch (message.role()) {
            case USER -> "user";
            case ASSISTANT -> "assistant";
        };

        return new AnthropicChatRequest.Message(
                role,
                message.content()
        );
    }

    private UnifiedChatResponse toUnifiedResponse(AnthropicChatResponse response) {
        if (response == null) {
            throw new IllegalStateException("Anthropic response must not be null");
        }

        return new UnifiedChatResponse(
                LlmProvider.ANTHROPIC,
                response.model(),
                response.firstText(),
                response.stopReason(),
                toTokenUsage(response.usage()),
                toMetadata(response)
        );
    }

    private TokenUsage toTokenUsage(AnthropicChatResponse.Usage usage) {
        if (usage == null) {
            return TokenUsage.empty();
        }

        return TokenUsage.of(
                usage.inputTokens(),
                usage.outputTokens()
        );
    }

    private Map<String, Object> toMetadata(AnthropicChatResponse response) {
        Map<String, Object> metadata = new LinkedHashMap<>();

        putIfNotNull(metadata, "id", response.id());
        putIfNotNull(metadata, "type", response.type());
        putIfNotNull(metadata, "role", response.role());
        putIfNotNull(metadata, "stopSequence", response.stopSequence());

        return metadata;
    }

    private void putIfNotNull(Map<String, Object> metadata, String key, Object value) {
        if (value != null) {
            metadata.put(key, value);
        }
    }

    private Mono<? extends Throwable> toException(ClientResponse response, String message) {
        return response.bodyToMono(String.class)
                .defaultIfEmpty("")
                .map(body -> new LlmProviderException(
                        provider,
                        response.statusCode().value(),
                        message,
                        body
                ));
    }

    private boolean isRetryable(Throwable throwable) {
        Throwable ex = Exceptions.unwrap(throwable);

        if (ex instanceof TimeoutException) {
            return true;
        }

        if (ex instanceof WebClientRequestException) {
            return true;
        }

        if (ex instanceof LlmProviderException providerException) {
            int status = providerException.statusCode();

            return status == 429
                    || status == 500
                    || status == 502
                    || status == 503
                    || status == 504;
        }

        return false;
    }
}
```
