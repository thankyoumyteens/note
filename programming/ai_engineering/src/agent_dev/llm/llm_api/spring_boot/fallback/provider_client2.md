# OpenAiResponsesProviderClient

Responses API 使用 `POST /v1/responses`。

和 Chat Completions 最大区别是：它没有 `choices[].message.content`，普通文本通常在 `output[].content[]` 里，`type = output_text`。

## OpenAiResponsesRequest

```java
package com.example.llm.dto.openai;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * OpenAI Responses API 请求体。
 * input 这里使用 messages 数组，方便兼容多轮对话历史。
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record OpenAiResponsesRequest(
        String model, // 要调用的模型名称。
        String instructions, // system / developer 类指令，用于设置模型行为和回答边界。
        List<ResponseInputMessage> input, // 输入消息列表，用于承载 user / assistant 多轮对话历史。
        Double temperature, // 控制模型输出随机性，值越低越稳定，值越高越发散。

        @JsonProperty("max_output_tokens")
        Integer maxOutputTokens, // 限制模型最多生成的 token 数，只限制输出长度。

        Boolean stream, // 是否启用流式输出。

        @JsonProperty("previous_response_id")
        String previousResponseId // 上一轮 response id，用于让 Responses API 续接上下文。
) {

    /**
     * Responses API 的输入消息。
     * role 通常是 user / assistant。
     */
    public record ResponseInputMessage(
            String role, // 消息角色，通常是 user 或 assistant。
            String content // 消息文本内容。
    ) {
    }
}
```

这里用了 `input` 数组，而不是单个字符串，是为了让 `UnifiedChatRequest.messages()` 可以直接转换成 Responses API 的多轮输入。Responses API 也可以用 `previous_response_id` 续接上一轮 response，但这需要你额外保存上一轮 `response.id`。

## OpenAiResponsesResponse

```java
package com.example.llm.dto.openai;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * OpenAI Responses API 的响应体。
 * 保留回答文本、模型名、状态、token usage 和基础元数据。
 */
public record OpenAiResponsesResponse(
        String id, // 响应 ID。
        String object, // 响应对象类型。

        @JsonProperty("created_at")
        Long createdAt, // 响应创建时间，通常是 Unix 时间戳。

        String status, // 响应状态，例如 completed、failed、incomplete。
        String model, // 实际使用的模型名称。
        List<OutputItem> output, // 模型输出项列表。
        Usage usage, // 本次调用的 token 用量信息。
        ErrorInfo error, // 响应失败时的错误信息。

        @JsonProperty("incomplete_details")
        IncompleteDetails incompleteDetails // 响应未完整生成时的详细原因。
) {

    /**
     * 获取所有 output_text 文本。
     * 如果响应为空或没有文本，则返回空字符串，避免空指针异常。
     */
    public String firstText() {
        if (output == null || output.isEmpty()) {
            return "";
        }

        StringBuilder builder = new StringBuilder();

        for (OutputItem outputItem : output) {
            if (outputItem.content() == null || outputItem.content().isEmpty()) {
                continue;
            }

            for (ContentItem contentItem : outputItem.content()) {
                if ("output_text".equals(contentItem.type()) && contentItem.text() != null) {
                    builder.append(contentItem.text());
                }
            }
        }

        return builder.toString();
    }

    /**
     * Responses API 没有 Chat Completions 那种 finish_reason。
     * 这里统一映射为：
     * - incomplete 时返回 incomplete_details.reason
     * - 其它情况返回 status
     */
    public String firstFinishReason() {
        if (incompleteDetails != null && incompleteDetails.reason() != null) {
            return incompleteDetails.reason();
        }

        return status;
    }

    /**
     * 单个输出项。
     * 普通文本回答一般是 type = message。
     */
    public record OutputItem(
            String id, // 输出项 ID。
            String type, // 输出项类型，普通文本回答通常是 message。
            String status, // 输出项状态。
            String role, // 输出消息角色，通常是 assistant。
            List<ContentItem> content // 输出内容块列表。
    ) {
    }

    /**
     * 输出内容块。
     * 普通文本结果通常是 type = output_text。
     */
    public record ContentItem(
            String type, // 内容块类型，普通文本通常是 output_text。
            String text // 输出文本内容。
    ) {
    }

    /**
     * Token 用量信息。
     * inputTokens 是输入 token，outputTokens 是输出 token。
     */
    public record Usage(
            @JsonProperty("input_tokens")
            Integer inputTokens, // 输入 token 数。

            @JsonProperty("output_tokens")
            Integer outputTokens, // 输出 token 数。

            @JsonProperty("total_tokens")
            Integer totalTokens // 输入和输出 token 总数。
    ) {
    }

    /**
     * Responses API 错误信息。
     * 当 status = failed 时，error 可能有值。
     */
    public record ErrorInfo(
            String code, // 错误码。
            String message // 错误消息。
    ) {
    }

    /**
     * Responses API 未完整生成时的原因。
     * 例如 max_output_tokens 等。
     */
    public record IncompleteDetails(
            String reason // 未完整生成的原因。
    ) {
    }
}
```

## OpenAiResponsesProviderClient

```java
package com.example.llm.provider;

import com.example.llm.dto.*;
import com.example.llm.dto.openai.OpenAiResponsesRequest;
import com.example.llm.dto.openai.OpenAiResponsesResponse;
import com.example.llm.exceptions.LlmProviderException;
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
import java.util.concurrent.atomic.AtomicInteger;

/**
 * OpenAI Responses API Provider 客户端。
 * 适用于 OpenAI 官方 /responses 接口。
 */
public class OpenAiResponsesProviderClient implements LlmProviderClient {

    // provider 标识，例如 openai。
    private final String provider;

    // OpenAI API Key。
    private final String apiKey;

    // 当前 provider 默认使用的模型名称。
    private final String model;

    // 整个请求的外层超时时间，防止 Mono 长时间不结束。
    private final int requestTimeoutSeconds;

    // 最大重试次数，只对临时错误生效。
    private final int maxRetries;

    // 当前 provider 专用的 WebClient。
    private final WebClient webClient;

    public OpenAiResponsesProviderClient(
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
        // 将业务层统一请求转换成 OpenAI Responses API 请求体。
        OpenAiResponsesRequest providerRequest = toOpenAiResponsesRequest(request);

        return Mono.defer(() -> {
            AtomicInteger retryCount = new AtomicInteger();

            return webClient.post()
                // OpenAI Responses API 路径。
                .uri("/responses")
                // OpenAI 官方认证方式：Authorization: Bearer xxx。
                .header(HttpHeaders.AUTHORIZATION, "Bearer " + apiKey)
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(providerRequest)
                .retrieve()
                // 将 HTTP 4xx / 5xx 转成统一的 LlmProviderException。
                .onStatus(
                        HttpStatusCode::isError,
                        response -> toException(response, "Provider server error")
                )
                // 将 provider 原始响应反序列化为 OpenAiResponsesResponse。
                .bodyToMono(OpenAiResponsesResponse.class)
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

    /**
     * 将统一聊天请求转换成 OpenAI Responses API 请求。
     */
    private OpenAiResponsesRequest toOpenAiResponsesRequest(UnifiedChatRequest request) {
        List<OpenAiResponsesRequest.ResponseInputMessage> input = new ArrayList<>();

        // Responses API 的 input 可以承载多轮 user / assistant 历史消息。
        for (UnifiedChatMessage message : request.messages()) {
            input.add(new OpenAiResponsesRequest.ResponseInputMessage(
                    toResponseRole(message.role()),
                    message.content()
            ));
        }

        return new OpenAiResponsesRequest(
                model,
                request.system(),
                input,
                request.options().temperature(),
                request.options().maxTokens(),
                false,
                null
        );
    }

    /**
     * 将业务层角色枚举映射成 Responses API 使用的 role 字符串。
     */
    private String toResponseRole(ChatRole role) {
        return switch (role) {
            case USER -> "user";
            case ASSISTANT -> "assistant";
        };
    }

    /**
     * 将 OpenAI Responses API 原始响应转换成业务层统一响应。
     */
    private UnifiedChatResponse toUnifiedResponse(OpenAiResponsesResponse response) {
        if (response == null) {
            throw new IllegalStateException("OpenAI Responses response must not be null");
        }

        // Responses API 即使 HTTP 是 200，也可能在响应体里返回 failed 状态。
        if ("failed".equals(response.status())) {
            throw new IllegalStateException("OpenAI Responses API returned failed status");
        }

        return new UnifiedChatResponse(
                toLlmProvider(),
                response.model() == null || response.model().isBlank() ? model : response.model(),
                response.firstText(),
                toStopReason(response.firstFinishReason()),
                toTokenUsage(response.usage()),
                toMetadata(response)
        );
    }

    private UnifiedStopReason toStopReason(String reason) {
        if (reason == null) {
            return null;
        }

        return switch (reason) {
            case "completed" -> UnifiedStopReason.STOP;
            case "max_output_tokens" -> UnifiedStopReason.LENGTH;
            case "content_filter" -> UnifiedStopReason.CONTENT_FILTER;
            default -> UnifiedStopReason.OTHER;
        };
    }

    /**
     * 将字符串 provider 映射成业务层枚举。
     * Responses API 当前只支持 OpenAI 官方 provider。
     */
    private LlmProvider toLlmProvider() {
        return switch (provider) {
            case "openai" -> LlmProvider.OPENAI;
            default -> throw new IllegalStateException("Unsupported OpenAI Responses provider: " + provider);
        };
    }

    /**
     * 将 Responses API usage 转换成统一 token usage。
     */
    private TokenUsage toTokenUsage(OpenAiResponsesResponse.Usage usage) {
        if (usage == null) {
            return TokenUsage.empty();
        }

        Integer inputTokens = usage.inputTokens();
        Integer outputTokens = usage.outputTokens();
        Integer totalTokens = usage.totalTokens();

        // 有些场景可能不返回 total_tokens，这里做一次兜底计算。
        if (totalTokens == null && inputTokens != null && outputTokens != null) {
            totalTokens = inputTokens + outputTokens;
        }

        return new TokenUsage(
                inputTokens,
                outputTokens,
                totalTokens
        );
    }

    /**
     * 提取 Responses API 响应里的基础元数据。
     * 元数据主要用于日志、排查和观测，不参与主业务逻辑。
     */
    private Map<String, Object> toMetadata(OpenAiResponsesResponse response) {
        Map<String, Object> metadata = new LinkedHashMap<>();

        putIfNotNull(metadata, "id", response.id());
        putIfNotNull(metadata, "object", response.object());
        putIfNotNull(metadata, "createdAt", response.createdAt());
        putIfNotNull(metadata, "status", response.status());

        // incomplete_details 用于说明响应未完整生成的原因。
        if (response.incompleteDetails() != null) {
            putIfNotNull(
                    metadata,
                    "incompleteReason",
                    response.incompleteDetails().reason()
            );
        }

        // error 用于记录 Responses API 返回的失败详情。
        if (response.error() != null) {
            putIfNotNull(metadata, "errorCode", response.error().code());
            putIfNotNull(metadata, "errorMessage", response.error().message());
        }

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

`OpenAI Responses API` 版本有两个额外注意点：

```text
1. 不要按 choices[].message.content 解析响应。
   Responses API 普通文本在 output[].content[] 里，type 通常是 output_text。

2. 不要强行找 finish_reason。
   Responses API 更适合映射 status / incomplete_details.reason。
```
