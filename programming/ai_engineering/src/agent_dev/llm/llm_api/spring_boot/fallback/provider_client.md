# OpenAiCompatibleProviderClient

## 修改 OpenAiChatResponse

```java
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * OpenAI-compatible Chat Completions API 的响应体。
 * 保留回答文本、模型名、停止原因、token usage 和基础元数据。
 */
public record OpenAiChatResponse(
        String id,
        String object,
        Long created,
        String model,
        List<Choice> choices,
        Usage usage,

        @JsonProperty("system_fingerprint")
        String systemFingerprint
) {

    /**
     * 获取第一个候选回答的文本内容。
     * 如果响应为空或没有 content，则返回空字符串，避免空指针异常。
     */
    public String firstText() {
        Choice choice = firstChoice();

        if (choice == null || choice.message() == null || choice.message().content() == null) {
            return "";
        }

        return choice.message().content();
    }

    /**
     * 获取第一个候选回答的停止原因。
     * 常见值：stop、length、tool_calls、content_filter。
     */
    public String firstFinishReason() {
        Choice choice = firstChoice();

        return choice == null ? null : choice.finishReason();
    }

    /**
     * 获取第一个候选结果。
     * 普通聊天场景通常只取第一个候选结果。
     */
    public Choice firstChoice() {
        if (choices == null || choices.isEmpty()) {
            return null;
        }

        return choices.getFirst();
    }

    /**
     * 单个候选结果。
     * message 是模型返回的消息，finishReason 表示模型停止生成的原因。
     */
    public record Choice(
            Integer index,
            Message message,

            @JsonProperty("finish_reason")
            String finishReason
    ) {
    }

    /**
     * 模型返回的消息内容。
     * role 通常是 assistant，content 是最终回答文本。
     */
    public record Message(
            String role,
            String content
    ) {
    }

    /**
     * Token 用量信息。
     * promptTokens 是输入 token，completionTokens 是输出 token。
     */
    public record Usage(
            @JsonProperty("prompt_tokens")
            Integer promptTokens,

            @JsonProperty("completion_tokens")
            Integer completionTokens,

            @JsonProperty("total_tokens")
            Integer totalTokens
    ) {
    }
}
```

## OpenAiCompatibleProviderClient

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
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeoutException;

public class OpenAiCompatibleProviderClient implements LlmProviderClient {

    private final String provider;
    private final String apiKey;
    private final String model;
    private final int requestTimeoutSeconds;
    private final int maxRetries;
    private final WebClient webClient;

    public OpenAiCompatibleProviderClient(
            String provider,
            String baseUrl,
            String apiKey,
            String model,
            int requestTimeoutSeconds,
            int maxRetries,
            int connectTimeoutMillis,
            int responseTimeoutSeconds
    ) {
        this.provider = provider;
        this.apiKey = apiKey;
        this.model = model;
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
        OpenAiChatRequest providerRequest = toOpenAiRequest(request);

        return webClient.post()
                .uri("/chat/completions")
                .header(HttpHeaders.AUTHORIZATION, "Bearer " + apiKey)
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(providerRequest)
                .retrieve()
                .onStatus(
                        HttpStatusCode::isError,
                        response -> toException(response, "Provider server error")
                )
                .bodyToMono(OpenAiChatResponse.class)
                // 整个 Mono 调用级超时，作为外层兜底。
                .timeout(Duration.ofSeconds(requestTimeoutSeconds))
                // 只重试临时错误。
                .retryWhen(
                        Retry.backoff(maxRetries, Duration.ofMillis(500))
                                .maxBackoff(Duration.ofSeconds(3))
                                .jitter(0.2)
                                .filter(this::isRetryable)
                                .onRetryExhaustedThrow((spec, signal) -> signal.failure())
                )
                .map(this::toUnifiedResponse);
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

        switch (ex) {
            case TimeoutException timeoutException -> {
                return true;
            }
            case WebClientRequestException webClientRequestException -> {
                return true;
            }
            case LlmProviderException providerException -> {
                int status = providerException.statusCode();

                return status == 429
                        || status == 500
                        || status == 502
                        || status == 503
                        || status == 504;
            }
            default -> {
            }
        }

        return false;
    }

    private OpenAiChatRequest toOpenAiRequest(UnifiedChatRequest request) {
        List<LlmMessage> messages = new ArrayList<>();

        if (request.system() != null && !request.system().isBlank()) {
            messages.add(new LlmMessage("system", request.system()));
        }

        for (UnifiedChatMessage message : request.messages()) {
            messages.add(new LlmMessage(
                    message.role() == ChatRole.USER ? "user" : "assistant",
                    message.content()
            ));
        }

        return new OpenAiChatRequest(
                model,
                messages,
                request.options().temperature(),
                request.options().maxTokens(),
                false
        );
    }

    private UnifiedChatResponse toUnifiedResponse(OpenAiChatResponse response) {
        if (response == null) {
            throw new IllegalStateException("OpenAI-compatible response must not be null");
        }

        return new UnifiedChatResponse(
                toLlmProvider(),
                response.model(),
                response.firstText(),
                response.firstFinishReason(),
                toTokenUsage(response.usage()),
                toMetadata(response)
        );
    }

    private LlmProvider toLlmProvider() {
        return switch (provider) {
            case "openai" -> LlmProvider.OPENAI;
            case "deepseek" -> LlmProvider.DEEPSEEK;
            default -> throw new IllegalStateException("Unsupported OpenAI-compatible provider: " + provider);
        };
    }

    private TokenUsage toTokenUsage(OpenAiChatResponse.Usage usage) {
        if (usage == null) {
            return TokenUsage.empty();
        }

        Integer inputTokens = usage.promptTokens();
        Integer outputTokens = usage.completionTokens();
        Integer totalTokens = usage.totalTokens();

        if (totalTokens == null && inputTokens != null && outputTokens != null) {
            totalTokens = inputTokens + outputTokens;
        }

        return new TokenUsage(
                inputTokens,
                outputTokens,
                totalTokens
        );
    }

    private Map<String, Object> toMetadata(OpenAiChatResponse response) {
        Map<String, Object> metadata = new LinkedHashMap<>();

        putIfNotNull(metadata, "id", response.id());
        putIfNotNull(metadata, "object", response.object());
        putIfNotNull(metadata, "created", response.created());
        putIfNotNull(metadata, "systemFingerprint", response.systemFingerprint());

        return metadata;
    }

    private void putIfNotNull(Map<String, Object> metadata, String key, Object value) {
        if (value != null) {
            metadata.put(key, value);
        }
    }
}
```

规则固定为：

```text
400：不重试，不降级
401：不重试，不降级
403：默认不重试，不降级
429：重试，失败后降级
5xx：重试，失败后降级
timeout / connection error：重试，失败后降级
```

`403` 是否降级要谨慎。工程上默认不降级，避免掩盖权限配置错误。只有当你能识别 provider 返回的是“模型未开通 / 当前模型不可用”这类可替代错误时，才允许降级。
