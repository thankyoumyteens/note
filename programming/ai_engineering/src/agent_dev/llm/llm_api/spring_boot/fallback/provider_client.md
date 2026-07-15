# OpenAiCompatibleProviderClient

## OpenAiChatRequest

```java
package com.example.llm.dto.openai;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * OpenAI-compatible Chat Completions API 的请求体 DTO。
 * 适用于 OpenAI 风格的 /chat/completions 接口。
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record OpenAiChatRequest(
        String model, // 要调用的模型名称。
        List<Message> messages, // 对话消息列表，包含 system、user、assistant 等角色消息。
        Double temperature, // 控制模型输出随机性，值越低越稳定，值越高越发散。
        @JsonProperty("max_tokens") Integer maxTokens, // 限制模型最多生成的 token 数，只限制输出长度。
        Boolean stream // 是否启用流式输出。
) {
    /**
     * 统一的 LLM 消息对象，用于表示一条对话消息。
     * role 表示消息角色，content 表示消息内容。
     */
    public record Message(
            String role,
            String content
    ) {
    }
}
```

## OpenAiChatResponse

```java
package com.example.llm.dto.openai;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * OpenAI-compatible Chat Completions API 的响应体。
 * 保留回答文本、模型名、停止原因、token usage 和基础元数据。
 */
public record OpenAiChatResponse(
        String id, // 响应 ID。
        String object, // 响应对象类型。
        Long created, // 响应创建时间，通常是 Unix 时间戳。
        String model, // 实际使用的模型名称。
        List<Choice> choices, // 候选回答列表。
        Usage usage, // 本次调用的 token 用量信息。

        @JsonProperty("system_fingerprint")
        String systemFingerprint // OpenAI 系统指纹，用于标识后端配置版本。
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
            Integer index, // 候选结果索引。
            Message message, // 模型返回的消息内容。

            @JsonProperty("finish_reason")
            String finishReason // 模型停止生成的原因。
    ) {
    }

    /**
     * 模型返回的消息内容。
     * role 通常是 assistant，content 是最终回答文本。
     */
    public record Message(
            String role, // 消息角色，通常是 assistant。
            String content // 模型返回的最终文本内容。
    ) {
    }

    /**
     * Token 用量信息。
     * promptTokens 是输入 token，completionTokens 是输出 token。
     */
    public record Usage(
            @JsonProperty("prompt_tokens")
            Integer promptTokens, // 输入 token 数。

            @JsonProperty("completion_tokens")
            Integer completionTokens, // 输出 token 数。

            @JsonProperty("total_tokens")
            Integer totalTokens // 输入和输出 token 总数。
    ) {
    }
}
```

## OpenAiCompatibleProviderClient

```java
package com.example.llm.provider;

import com.example.llm.exceptions.LlmProviderException;
import com.example.llm.dto.*;
import com.example.llm.dto.openai.OpenAiChatRequest;
import com.example.llm.dto.openai.OpenAiChatResponse;
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

/**
 * OpenAI-compatible Provider 客户端。
 * 适用于 OpenAI / DeepSeek 等兼容 /chat/completions 协议的模型服务。
 */
public class OpenAiCompatibleProviderClient implements LlmProviderClient {

    // provider 标识，例如 openai / deepseek。
    private final String provider;

    // 当前 provider 的 API Key。
    private final String apiKey;

    // 当前 provider 默认使用的模型名称。
    private final String model;

    // 整个请求的外层超时时间，防止 Mono 长时间不结束。
    private final int requestTimeoutSeconds;

    // 最大重试次数，只对临时错误生效。
    private final int maxRetries;

    // 当前 provider 专用的 WebClient。
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
        // 将业务层统一请求转换成 OpenAI-compatible 请求体。
        OpenAiChatRequest providerRequest = toOpenAiRequest(request);

        return webClient.post()
                // OpenAI-compatible Chat Completions API 路径。
                .uri("/chat/completions")
                // OpenAI 风格认证方式：Authorization: Bearer xxx。
                .header(HttpHeaders.AUTHORIZATION, "Bearer " + apiKey)
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(providerRequest)
                .retrieve()
                // 将 HTTP 4xx / 5xx 转成统一的 LlmProviderException。
                .onStatus(
                        HttpStatusCode::isError,
                        response -> toException(response, "Provider server error")
                )
                // 将 provider 原始响应反序列化为 OpenAiChatResponse。
                .bodyToMono(OpenAiChatResponse.class)
                // 单次 provider 尝试的请求级总超时。
                .timeout(Duration.ofSeconds(requestTimeoutSeconds))
                // 只重试临时错误，例如超时、网络错误、429、5xx。
                .retryWhen(
                        Retry.backoff(maxRetries, Duration.ofMillis(500))
                                // 每次重试的等待时间按指数退避增长，但最大不超过 3 秒。
                                .maxBackoff(Duration.ofSeconds(3))
                                // 给退避时间增加 20% 随机抖动，避免多个请求同时重试造成雪崩。
                                .jitter(0.2)
                                // 只有 isRetryable 返回 true 才会重试。
                                .filter(this::isRetryable)
                                // 重试次数耗尽后，继续抛出最后一次失败的原始异常。
                                .onRetryExhaustedThrow((spec, signal) -> signal.failure())
                )
                // 将 provider 原始响应转换成业务层统一响应。
                .map(this::toUnifiedResponse);
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
     * 将统一聊天请求转换成 OpenAI-compatible Chat Completions 请求。
     */
    private OpenAiChatRequest toOpenAiRequest(UnifiedChatRequest request) {
        List<OpenAiChatRequest.Message> messages = new ArrayList<>();

        // OpenAI-compatible API 通常把 system 作为 messages 里的第一条 system 消息。
        if (request.system() != null && !request.system().isBlank()) {
            messages.add(new OpenAiChatRequest.Message("system", request.system()));
        }

        // 将业务层统一消息角色映射成 OpenAI-compatible 的 role 字符串。
        for (UnifiedChatMessage message : request.messages()) {
            messages.add(new OpenAiChatRequest.Message(
                    message.role() == ChatRole.USER ? "user" : "assistant",
                    message.content()
            ));
        }

        return new OpenAiChatRequest(
                model,
                messages,
                request.options().temperature(),
                request.options().maxTokens(),
                false // 非流式
        );
    }

    /**
     * 将 OpenAI-compatible 原始响应转换成业务层统一响应。
     */
    private UnifiedChatResponse toUnifiedResponse(OpenAiChatResponse response) {
        if (response == null) {
            throw new IllegalStateException("OpenAI-compatible response must not be null");
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
            case "stop" -> UnifiedStopReason.STOP;
            case "length" -> UnifiedStopReason.LENGTH;
            case "tool_calls" -> UnifiedStopReason.TOOL_CALLS;
            case "content_filter" -> UnifiedStopReason.CONTENT_FILTER;
            default -> UnifiedStopReason.OTHER;
        };
    }

    /**
     * 将字符串 provider 映射成业务层枚举。
     * 当前 OpenAI-compatible 客户端只允许 openai / deepseek。
     */
    private LlmProvider toLlmProvider() {
        return switch (provider) {
            case "openai" -> LlmProvider.OPENAI;
            case "deepseek" -> LlmProvider.DEEPSEEK;
            default -> throw new IllegalStateException("Unsupported OpenAI-compatible provider: " + provider);
        };
    }

    /**
     * 将 OpenAI-compatible usage 转换成统一 token usage。
     */
    private TokenUsage toTokenUsage(OpenAiChatResponse.Usage usage) {
        if (usage == null) {
            return TokenUsage.empty();
        }

        Integer inputTokens = usage.promptTokens();
        Integer outputTokens = usage.completionTokens();
        Integer totalTokens = usage.totalTokens();

        // 有些兼容 provider 可能不返回 total_tokens，这里做一次兜底计算。
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
     * 提取 provider 响应里的基础元数据。
     * 元数据不参与主业务逻辑，主要用于日志、排查和观测。
     */
    private Map<String, Object> toMetadata(OpenAiChatResponse response) {
        Map<String, Object> metadata = new LinkedHashMap<>();

        putIfNotNull(metadata, "id", response.id());
        putIfNotNull(metadata, "object", response.object());
        putIfNotNull(metadata, "created", response.created());
        putIfNotNull(metadata, "systemFingerprint", response.systemFingerprint());
        putIfNotNull(metadata, "rawStopReason", response.firstFinishReason());

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

`403` 是否降级要谨慎。工程上默认不降级，避免掩盖权限配置错误。只有当你能识别 provider 返回的是“模型未开通 / 当前模型不可用”这类可替代错误时，才允许降级。
