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

## OpenAiChatStreamResponse

```java
package com.example.llm.dto.openai;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * OpenAI-compatible Chat Completions Stream API 的单个 SSE chunk 响应体。
 * 流式响应中，文本通常出现在 choices[].delta.content，而不是 choices[].message.content。
 */
public record OpenAiChatStreamResponse(
        String id, // 流式响应 ID，同一次流式请求的多个 chunk 通常使用相同 ID。
        String object, // 响应对象类型，流式场景通常是 chat.completion.chunk。
        Long created, // 响应创建时间，通常是 Unix 时间戳。
        String model, // 实际使用的模型名称。
        List<Choice> choices, // 本次 chunk 中的候选增量列表。
        Usage usage, // token 用量信息，通常只在最终统计 chunk 中出现，普通增量 chunk 可能为空。

        @JsonProperty("system_fingerprint")
        String systemFingerprint // OpenAI 系统指纹，用于标识后端服务配置版本，部分 provider 可能不返回。
) {

    /**
     * 获取第一个候选结果的增量文本。
     * 如果当前 chunk 没有 content，则返回空字符串。
     */
    public String firstDeltaText() {
        if (choices == null || choices.isEmpty()) {
            return "";
        }

        Choice choice = choices.getFirst();

        if (choice.delta() == null || choice.delta().content() == null) {
            return "";
        }

        return choice.delta().content();
    }

    /**
     * 单个候选增量结果。
     * delta 是本次 chunk 的增量内容，finishReason 表示该候选是否结束生成。
     */
    public record Choice(
            Integer index, // 候选结果索引。
            Delta delta, // 本次 chunk 返回的增量消息内容。

            @JsonProperty("finish_reason")
            String finishReason // 停止原因；中间 chunk 通常为空，结束 chunk 可能是 stop、length、tool_calls 等。
    ) {
    }

    /**
     * 流式增量消息内容。
     * role 通常只在开头 chunk 出现，content 通常在后续文本 chunk 中逐段出现。
     */
    public record Delta(
            String role, // 增量消息角色，通常只在第一个 chunk 中出现 assistant。
            String content // 本次 chunk 返回的增量文本内容，不是完整最终回答。
    ) {
    }

    /**
     * Token 用量信息。
     * 流式场景下 usage 通常不会出现在每个 chunk 中，只有开启相关 stream options 后才可能在最终统计 chunk 中返回。
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

## OpenAiCompatibleStreamProviderClient

在 LLM stream 中，最危险的问题是：模型已经输出了一部分内容，连接突然断了。

例如前端已经收到了：

```text
RAG 是一种结合检索和生成的技术...
```

这时如果直接 retry，模型可能从头重新生成，前端就会收到重复或混乱内容。

所以需要一个标记：contentStarted = 是否已经输出过 message chunk。

规则是：

- 还没输出任何文本：可以 retry
- 已经输出过文本：
  - 不 retry
  - 不 fallback
  - 直接 error 结束

```java
package com.example.llm.provider;

import com.example.llm.dto.LlmProvider;
import com.example.llm.dto.UnifiedChatMessage;
import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatStreamEvent;
import com.example.llm.dto.openai.OpenAiChatRequest;
import com.example.llm.dto.openai.OpenAiChatStreamResponse;
import com.example.llm.exceptions.LlmProviderException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientRequestException;
import reactor.core.Exceptions;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.util.retry.Retry;

import java.time.Duration;
import java.util.List;
import java.util.concurrent.TimeoutException;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * OpenAI-compatible stream provider。
 * 当前 provider 内只在尚未输出内容前 retry，避免重复输出 chunk。
 */
public class OpenAiCompatibleStreamProviderClient implements LlmStreamProviderClient {

    // SSE 响应的反序列化类型，用于读取 data: xxx 形式的流式事件。
    private static final ParameterizedTypeReference<ServerSentEvent<String>> SSE_STRING =
            new ParameterizedTypeReference<>() {
            };

    // provider 配置名称，例如 openai、deepseek。
    private final String provider;

    // 统一 provider 枚举，用于输出 UnifiedChatStreamEvent。
    private final LlmProvider llmProvider;

    // 当前 provider 的 API Key。
    private final String apiKey;

    // 当前 provider 要调用的模型名称。
    private final String model;

    // 当前 provider 的接口路径，例如 /chat/completions。
    private final String path;

    // stream 空闲超时时间，超过该时间没有收到 chunk 就认为流中断。
    private final int streamIdleTimeoutSeconds;

    // 当前 provider 内部最大重试次数。
    private final int maxRetries;

    // 调用上游 provider 的 WebClient。
    private final WebClient webClient;

    // 用于解析 OpenAI-compatible stream chunk。
    private final ObjectMapper objectMapper;

    public OpenAiCompatibleStreamProviderClient(
            String provider,
            LlmProvider llmProvider,
            String baseUrl,
            String path,
            String apiKey,
            String model,
            int streamIdleTimeoutSeconds,
            int maxRetries,
            int connectTimeoutMillis,
            int responseTimeoutSeconds,
            ObjectMapper objectMapper
    ) {
        this.provider = provider;
        this.llmProvider = llmProvider;
        this.apiKey = apiKey;
        this.model = model;
        this.path = path;
        this.streamIdleTimeoutSeconds = streamIdleTimeoutSeconds;
        this.maxRetries = maxRetries;
        this.webClient = WebClientFactory.create(baseUrl, connectTimeoutMillis, responseTimeoutSeconds);
        this.objectMapper = objectMapper;
    }

    /**
     * 返回当前 ProviderClient 的配置名称。
     */
    @Override
    public String provider() {
        return provider;
    }

    /**
     * 发起流式调用。
     * 如果尚未输出任何内容，并且异常可重试，则在当前 provider 内部 retry。
     */
    @Override
    public Flux<UnifiedChatStreamEvent> stream(UnifiedChatRequest request) {
        // 标记当前 provider 是否已经输出过 message chunk。
        AtomicBoolean contentStarted = new AtomicBoolean(false);

        // defer 的作用：不要现在就创建真正的 Flux 执行逻辑，
        // 等到有人 subscribe 时，再执行 supplier 创建 Flux。
        return Flux.defer(() -> doStream(request, contentStarted))
                .retryWhen(
                        Retry.backoff(maxRetries, Duration.ofMillis(500))
                                // 限制最大退避时间，避免重试等待过久。
                                .maxBackoff(Duration.ofSeconds(3))
                                // 增加随机抖动，避免多个请求同时重试造成尖峰。
                                .jitter(0.2)
                                // 只有尚未输出内容，并且异常可重试时，才允许 retry。
                                .filter(ex -> !contentStarted.get() && isRetryable(ex))
                                // 重试耗尽后，把最后一次异常继续向外抛出。
                                .onRetryExhaustedThrow((spec, signal) -> signal.failure())
                );
    }

    /**
     * 执行真正的 WebClient stream 请求。
     */
    private Flux<UnifiedChatStreamEvent> doStream(
            UnifiedChatRequest request,
            AtomicBoolean contentStarted
    ) {
        // 把统一请求转换为 OpenAI-compatible Chat Completions 请求。
        OpenAiChatRequest providerRequest = toProviderRequest(request);

        return webClient.post()
                .uri(path)
                .header(HttpHeaders.AUTHORIZATION, "Bearer " + apiKey)
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.TEXT_EVENT_STREAM)
                .bodyValue(providerRequest)
                .retrieve()
                // 将 HTTP 错误状态转换成统一 provider 异常。
                .onStatus(
                        HttpStatusCode::isError,
                        response -> toException(response, "Provider server error")
                )
                // 按 SSE 格式读取上游流式响应。
                .bodyToFlux(SSE_STRING)
                // stream 空闲超时控制，防止连接长时间无响应。
                .timeout(Duration.ofSeconds(streamIdleTimeoutSeconds))
                // OpenAI-compatible stream 使用 [DONE] 表示流结束。
                .takeUntil(sse -> "[DONE]".equals(sse.data()))
                // 将 provider 原始 chunk 转换为统一 stream event。
                .flatMap(sse -> toUnifiedEvent(sse, contentStarted));
    }

    /**
     * 将统一请求转换为 OpenAI-compatible 请求。
     */
    private OpenAiChatRequest toProviderRequest(UnifiedChatRequest request) {
        List<OpenAiChatRequest.Message> messages = buildMessages(request);

        return new OpenAiChatRequest(
                model,
                messages,
                request.options().temperature(),
                request.options().maxTokens(),
                true
        );
    }

    /**
     * 构建 OpenAI-compatible messages。
     * system 会被放入 messages 首位。
     */
    private List<OpenAiChatRequest.Message> buildMessages(UnifiedChatRequest request) {
        List<OpenAiChatRequest.Message> messages = new java.util.ArrayList<>();

        // OpenAI-compatible API 通常把 system 指令放在 messages 中。
        if (request.system() != null && !request.system().isBlank()) {
            messages.add(new OpenAiChatRequest.Message("system", request.system()));
        }

        // 将统一消息列表逐条转换为 provider 消息。
        for (UnifiedChatMessage message : request.messages()) {
            messages.add(toOpenAiMessage(message));
        }

        return List.copyOf(messages);
    }

    /**
     * 将统一消息角色转换为 OpenAI-compatible 消息角色。
     */
    private OpenAiChatRequest.Message toOpenAiMessage(UnifiedChatMessage message) {
        String role = switch (message.role()) {
            case USER -> "user";
            case ASSISTANT -> "assistant";
        };

        return new OpenAiChatRequest.Message(role, message.content());
    }

    /**
     * 将单个 SSE chunk 转换为统一 stream event。
     */
    private Mono<UnifiedChatStreamEvent> toUnifiedEvent(
            ServerSentEvent<String> sse,
            AtomicBoolean contentStarted
    ) {
        String data = sse.data();

        // 空 chunk 不输出给下游。
        if (data == null || data.isBlank()) {
            return Mono.empty();
        }

        // 收到 [DONE] 后，输出统一 DONE 事件。
        if ("[DONE]".equals(data)) {
            return Mono.just(UnifiedChatStreamEvent.done(
                    llmProvider,
                    model,
                    com.example.llm.dto.TokenUsage.empty()
            ));
        }

        try {
            // 解析 OpenAI-compatible stream chunk。
            OpenAiChatStreamResponse response = objectMapper.readValue(data, OpenAiChatStreamResponse.class);

            // 提取当前 chunk 的增量文本。
            String text = response.firstDeltaText();

            // 没有文本的 chunk 不输出，例如 role chunk 或 finish chunk。
            if (text == null || text.isEmpty()) {
                return Mono.empty();
            }

            // 一旦输出过文本，就不再允许当前 provider retry。
            contentStarted.set(true);

            return Mono.just(UnifiedChatStreamEvent.message(
                    llmProvider,
                    model,
                    text
            ));

        } catch (Exception ex) {
            // JSON 解析失败时，包装成统一 provider 异常。
            return Mono.error(new LlmProviderException(
                    provider,
                    -1,
                    "Failed to parse OpenAI-compatible stream chunk",
                    data,
                    ex
            ));
        }
    }

    /**
     * 将 HTTP 错误响应转换为统一 provider 异常。
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
     * 判断异常是否允许在当前 provider 内部重试。
     */
    private boolean isRetryable(Throwable throwable) {
        Throwable ex = Exceptions.unwrap(throwable);

        // Reactor timeout 会表现为 TimeoutException。
        if (ex instanceof TimeoutException) {
            return true;
        }

        // 网络连接失败、DNS 失败、连接被拒绝等通常会表现为 WebClientRequestException。
        if (ex instanceof WebClientRequestException) {
            return true;
        }

        if (ex instanceof LlmProviderException providerException) {
            int status = providerException.statusCode();

            // -1 表示非 HTTP 状态错误，例如解析失败、网络异常包装等。
            return status == -1
                    || status == 429
                    || status == 500
                    || status == 502
                    || status == 503
                    || status == 504;
        }

        return false;
    }
}
```

## Flux.defer 是什么

`Flux.defer(...)` 的作用是：不要现在就创建真正的 Flux 执行逻辑，等到有人 subscribe 时，再执行 supplier 创建 Flux。

在 WebClient stream 中：

```text
Flux.defer(() -> doStream(request, contentStarted))
```

含义是：

```text
每次订阅时，才执行 doStream(...)
每次 retry 重新订阅时，也会重新执行 doStream(...)
```

也就是说：

```text
第一次 subscribe
  ↓
执行 doStream(...)
  ↓
发起第 1 次 provider stream 请求
  ↓
失败
  ↓
retryWhen 判断允许重试
  ↓
重新 subscribe
  ↓
再次执行 doStream(...)
  ↓
发起第 2 次 provider stream 请求
```

## 为什么 retry 场景需要 Flux.defer

`retryWhen` 的本质是：

```text
上游失败后，重新 subscribe 上游
```

如果使用：

```text
Flux.defer(() -> doStream(...)).retryWhen(...)
```

那么每次 retry 都会重新执行 `doStream(...)`，也就是重新创建一次 WebClient stream 请求。

这对 stream 请求很重要，因为每次重试都应该是一次新的 HTTP 请求，而不是复用旧的失败流。

## 为什么非流式的 retry 不需要 Flux.defer

非流式调用因为 `WebClient` 返回的 `Mono` 本身就是冷流(只有被订阅 subscribe 时，才真正开始执行的数据流)，`retryWhen` 重新订阅时会重新发起 HTTP 请求，而且没有“已经输出一半内容”的风险，所以不强制需要 `Mono.defer`。

非流式也建议加 Mono.defer 的情况：

1. 每次 retry 都要重新生成 requestId / traceId
2. 每次 retry 都要重新读取动态配置
3. 请求体里有一次性资源
4. 请求构造逻辑有副作用
5. 希望非 stream 和 stream ProviderClient 风格统一
