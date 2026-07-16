# AnthropicProviderClient

## AnthropicChatRequest

```java
package com.example.llm.dto.anthropic;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * Anthropic Messages API 请求体。
 * system 是顶层字段，messages 只放 user / assistant。
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record AnthropicChatRequest(
        String model, // 要调用的 Claude 模型名称。

        @JsonProperty("max_tokens")
        Integer maxTokens, // 限制模型最多生成的 token 数，只限制输出长度。
        Double temperature, // 控制模型输出随机性，值越低越稳定，值越高越发散。

        @JsonProperty("top_p")
        Double topP, // nucleus sampling 参数，用于控制候选 token 的采样范围。
        String system, // 系统指令，用于设置模型行为和回答边界。
        List<Message> messages, // 对话消息列表，只包含 user / assistant 消息。
        Boolean stream // 是否启用流式输出。
) {

    /**
     * Anthropic message。
     * role 只能是 user 或 assistant。
     */
    public record Message(
            String role, // 消息角色，只能是 user 或 assistant。
            String content // 消息文本内容。
    ) {
    }
}
```

## AnthropicChatResponse

```java
package com.example.llm.dto.anthropic;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * Anthropic Messages API 响应体。
 * content 是数组，文本结果通常在 type=text 的 content block 里。
 */
public record AnthropicChatResponse(
        String id, // 响应 ID。
        String type, // 响应类型，通常是 message。
        String role, // 返回消息角色，通常是 assistant。
        String model, // 实际使用的 Claude 模型名称。
        List<ContentBlock> content, // 输出内容块列表，可能包含 text / thinking / tool_use 等类型。

        @JsonProperty("stop_reason")
        String stopReason, // 模型停止生成的原因，例如 end_turn、max_tokens、stop_sequence。

        @JsonProperty("stop_sequence")
        String stopSequence, // 命中的自定义停止序列，没有命中时通常为空。

        Usage usage // 本次调用的 token 用量信息。
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
            String type, // 内容块类型，普通文本通常是 text。
            String text // 文本内容，仅 type=text 时通常有值。
    ) {
    }

    /**
     * Anthropic token usage。
     */
    public record Usage(
            @JsonProperty("input_tokens")
            Integer inputTokens, // 输入 token 数。

            @JsonProperty("output_tokens")
            Integer outputTokens // 输出 token 数。
    ) {
    }
}
```

## AnthropicProviderClient

```java
package com.example.llm.provider;

import com.example.llm.exceptions.LlmProviderException;
import com.example.llm.dto.LlmProvider;
import com.example.llm.dto.TokenUsage;
import com.example.llm.dto.UnifiedChatMessage;
import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatResponse;
import com.example.llm.dto.UnifiedStopReason;
import com.example.llm.dto.anthropic.AnthropicChatRequest;
import com.example.llm.dto.anthropic.AnthropicChatResponse;
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
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Anthropic Messages API provider client。
 * 负责 Anthropic 协议转换、HTTP 错误处理、timeout 和 retry。
 */
public class AnthropicProviderClient implements LlmProviderClient {

    // provider 标识，例如 anthropic。
    private final String provider;

    // Anthropic API Key。
    private final String apiKey;

    // 当前 provider 默认使用的 Claude 模型名称。
    private final String model;

    // Anthropic API 版本，例如 2023-06-01。
    private final String anthropicVersion;

    // 整个请求的外层超时时间，防止 Mono 长时间不结束。
    private final int requestTimeoutSeconds;

    // 最大重试次数，只对临时错误生效。
    private final int maxRetries;

    // 当前 provider 专用的 WebClient。
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

        // 通过工厂创建 WebClient，统一处理连接超时和响应超时。
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
        // 将业务层统一请求转换成 Anthropic Messages API 请求体。
        AnthropicChatRequest providerRequest = toAnthropicRequest(request);

        return Mono.defer(() -> {
            AtomicInteger retryCount = new AtomicInteger();

            return webClient.post()
                // Anthropic Messages API 路径。
                .uri("/messages")
                // Anthropic 使用 x-api-key 作为认证请求头。
                .header("x-api-key", apiKey)
                // Anthropic 要求显式传入 API version。
                .header("anthropic-version", anthropicVersion)
                .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .bodyValue(providerRequest)
                .retrieve()
                // 将 HTTP 4xx / 5xx 转成统一的 LlmProviderException。
                .onStatus(
                        HttpStatusCode::isError,
                        response -> toException(response, "Provider server error")
                )
                // 将 provider 原始响应反序列化为 AnthropicChatResponse。
                .bodyToMono(AnthropicChatResponse.class)
                // 单次 provider 尝试的请求级总超时。
                .timeout(Duration.ofSeconds(requestTimeoutSeconds))
                // 只重试临时错误，例如超时、网络错误、429、5xx。
                .retryWhen(
                        Retry.backoff(maxRetries, Duration.ofMillis(500))
                                // 指数退避的最大等待时间，避免重试间隔无限变长。
                                .maxBackoff(Duration.ofSeconds(3))
                                // 增加随机抖动，降低并发请求同时重试的概率。
                                .jitter(0.2)
                                // 只重试临时性错误，不重试参数错误、认证错误、权限错误。
                                .filter(this::isRetryable)
                                // 每次真正重试前累加，首次请求不计入 retryCount。
                                .doBeforeRetry(signal -> retryCount.incrementAndGet())
                                // 重试耗尽后抛出最后一次异常，交给上层降级链或全局异常处理。
                                .onRetryExhaustedThrow((spec, signal) -> signal.failure())
                )
                // 将 provider 原始响应转换成业务层统一响应。
                .map(this::toUnifiedResponse)
                .map(response -> withRetryCount(response, retryCount.get()))
                .onErrorMap(error -> withRetryCount(error, retryCount.get()));
        });
    }

    private UnifiedChatResponse withRetryCount(UnifiedChatResponse response, int retryCount) {
        Map<String, Object> metadata = new LinkedHashMap<>(response.metadata());
        metadata.put("retryCount", retryCount);

        return new UnifiedChatResponse(
                response.provider(), response.model(), response.content(), response.stopReason(),
                response.usage(), metadata
        );
    }

    private Throwable withRetryCount(Throwable throwable, int retryCount) {
        Throwable error = Exceptions.unwrap(throwable);

        if (error instanceof LlmProviderException providerError) {
            return new LlmProviderException(
                    providerError.provider(), providerError.statusCode(), providerError.getMessage(),
                    providerError.responseBody(), providerError.getCause(), retryCount
            );
        }

        return new LlmProviderException(
                provider, -1, "Provider request failed", "", error, retryCount
        );
    }

    /**
     * 将统一聊天请求转换成 Anthropic Messages API 请求。
     */
    private AnthropicChatRequest toAnthropicRequest(UnifiedChatRequest request) {
        // Anthropic 的 messages 只放 user / assistant，不放 system。
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
                messages,
                false
        );
    }

    /**
     * 将业务层统一消息转换成 Anthropic message。
     */
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

    /**
     * 将 Anthropic 原始响应转换成业务层统一响应。
     */
    private UnifiedChatResponse toUnifiedResponse(AnthropicChatResponse response) {
        if (response == null) {
            throw new IllegalStateException("Anthropic response must not be null");
        }

        return new UnifiedChatResponse(
                LlmProvider.ANTHROPIC,
                response.model() == null || response.model().isBlank() ? model : response.model(),
                response.firstText(),
                toStopReason(response.stopReason()),
                toTokenUsage(response.usage()),
                toMetadata(response)
        );
    }

    private UnifiedStopReason toStopReason(String reason) {
        if (reason == null) {
            return null;
        }

        return switch (reason) {
            case "end_turn", "stop_sequence" -> UnifiedStopReason.STOP;
            case "max_tokens" -> UnifiedStopReason.LENGTH;
            case "tool_use" -> UnifiedStopReason.TOOL_CALLS;
            case "refusal" -> UnifiedStopReason.CONTENT_FILTER;
            default -> UnifiedStopReason.OTHER;
        };
    }

    /**
     * 将 Anthropic usage 转换成统一 token usage。
     */
    private TokenUsage toTokenUsage(AnthropicChatResponse.Usage usage) {
        if (usage == null) {
            return TokenUsage.empty();
        }

        return TokenUsage.of(
                usage.inputTokens(),
                usage.outputTokens()
        );
    }

    /**
     * 提取 Anthropic 响应里的基础元数据。
     * 元数据主要用于日志、排查和观测，不参与主业务逻辑。
     */
    private Map<String, Object> toMetadata(AnthropicChatResponse response) {
        Map<String, Object> metadata = new LinkedHashMap<>();

        putIfNotNull(metadata, "id", response.id());
        putIfNotNull(metadata, "type", response.type());
        putIfNotNull(metadata, "role", response.role());
        putIfNotNull(metadata, "stopSequence", response.stopSequence());
        putIfNotNull(metadata, "rawStopReason", response.stopReason());

        return metadata;
    }

    /**
     * 只写入非空元数据，避免 metadata 里出现大量 null。
     */
    private void putIfNotNull(Map<String, Object> metadata, String key, Object value) {
        if (value != null) {
            metadata.put(key, value);
        }
    }

    /**
     * 将 WebClient 的错误响应转换成统一异常。
     * response body 保留下来，方便日志排查 provider 返回的具体错误。
     */
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

    /**
     * 判断异常是否允许重试。
     * 只重试临时性错误，不重试 400 / 401 / 403 这类确定性错误。
     */
    private boolean isRetryable(Throwable throwable) {
        // Reactor 可能会包装异常，这里先拆出原始异常。
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
