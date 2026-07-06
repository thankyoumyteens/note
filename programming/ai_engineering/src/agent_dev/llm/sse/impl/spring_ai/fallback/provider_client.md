# SpringAiProviderClient

这里使用 `stream().chatResponse()`，而不是 `stream().content()`，因为 `ChatResponse` 可以携带 metadata。

```java id="b6m0hb"
package com.example.llm.provider;

import com.example.llm.dto.*;
import com.example.llm.exceptions.LlmProviderException;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.messages.Message;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.prompt.ChatOptions;
import org.springframework.web.client.RestClientResponseException;
import org.springframework.web.reactive.function.client.WebClientRequestException;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import reactor.core.Exceptions;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.util.retry.Retry;

import java.time.Duration;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeoutException;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;

/**
 * 基于 Spring AI ChatClient 的统一 stream provider。
 * Spring AI 负责 provider 协议适配，本类负责统一 DTO、retry、metadata 和事件转换。
 */
public class SpringAiStreamProviderClient implements LlmStreamProviderClient {

    // provider 配置名称，例如 openai、deepseek、anthropic。
    private final String provider;

    // 统一 provider 枚举，用于输出 UnifiedChatStreamEvent。
    private final LlmProvider llmProvider;

    // 当前 provider 要调用的模型名称。
    private final String model;

    // Spring AI ChatClient，负责实际调用底层模型服务。
    private final ChatClient chatClient;

    // stream 空闲超时时间，超过该时间没有收到 chunk 就认为流中断。
    private final int streamIdleTimeoutSeconds;

    // 当前 provider 内部最大重试次数。
    private final int maxRetries;

    public SpringAiStreamProviderClient(
            String provider,
            LlmProvider llmProvider,
            String model,
            ChatClient chatClient,
            int streamIdleTimeoutSeconds,
            int maxRetries
    ) {
        this.provider = provider;
        this.llmProvider = llmProvider;
        this.model = model;
        this.chatClient = chatClient;
        this.streamIdleTimeoutSeconds = streamIdleTimeoutSeconds;
        this.maxRetries = maxRetries;
    }

    /**
     * 返回当前 ProviderClient 的配置名称。
     */
    @Override
    public String provider() {
        return provider;
    }

    /**
     * 发起 Spring AI 流式调用。
     * 如果尚未输出任何文本，并且异常可重试，则在当前 provider 内部 retry。
     */
    @Override
    public Flux<UnifiedChatStreamEvent> stream(UnifiedChatRequest request) {
        // 标记当前 provider 是否已经输出过 message chunk。
        AtomicBoolean contentStarted = new AtomicBoolean(false);

        // defer 保证每次 subscribe / retry 时重新创建一次 Spring AI stream 调用。
        return Flux.defer(() -> doStream(request, contentStarted)
                        // 将 Spring AI / HTTP / Reactor 异常统一包装为 LlmProviderException。
                        .onErrorMap(ex -> toProviderException(provider, ex)))
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
     * 执行真正的 Spring AI stream 请求。
     */
    private Flux<UnifiedChatStreamEvent> doStream(
            UnifiedChatRequest request,
            AtomicBoolean contentStarted
    ) {
        // 保存最新 usage，部分 provider 可能只在某些 chunk 中返回 usage。
        AtomicReference<TokenUsage> latestUsage = new AtomicReference<>(TokenUsage.empty());

        // 保存最新 metadata，最终 DONE 事件会携带最后一次可用的 metadata。
        AtomicReference<Map<String, Object>> latestMetadata = new AtomicReference<>(Map.of());

        return chatClient.prompt()
                // 将统一消息结构转换为 Spring AI Message。
                .messages(toSpringAiMessages(request))
                // 将统一生成参数转换为 Spring AI ChatOptions。
                .options(toChatOptions(request))
                // 启用 Spring AI 流式调用。
                .stream()
                // 使用 chatResponse() 而不是 content()，以便读取 metadata 和 usage。
                .chatResponse()
                // stream 空闲超时控制，防止连接长时间无响应。
                .timeout(Duration.ofSeconds(streamIdleTimeoutSeconds))
                .doOnNext(response -> {
                    // 合并每个 chunk 中可能出现的 token usage。
                    latestUsage.set(mergeUsage(latestUsage.get(), toTokenUsage(response)));

                    // 保存当前 chunk 的 metadata，供最终 DONE 事件使用。
                    latestMetadata.set(toMetadata(response));
                })
                // 将 Spring AI ChatResponse 转换为统一 MESSAGE 事件。
                .flatMap(response -> toMessageEvent(response, contentStarted))
                // 上游正常结束后，追加一个统一 DONE 事件。
                .concatWith(Mono.fromSupplier(() -> UnifiedChatStreamEvent.done(
                        llmProvider,
                        model,
                        latestUsage.get(),
                        latestMetadata.get()
                )));
    }

    /**
     * 将统一聊天请求转换为 Spring AI 消息列表。
     */
    private List<Message> toSpringAiMessages(UnifiedChatRequest request) {
        List<Message> messages = new ArrayList<>();

        // system 指令转换为 Spring AI SystemMessage。
        if (request.system() != null && !request.system().isBlank()) {
            messages.add(new SystemMessage(request.system()));
        }

        // user / assistant 历史消息转换为 Spring AI Message。
        for (UnifiedChatMessage message : request.messages()) {
            messages.add(toSpringAiMessage(message));
        }

        return List.copyOf(messages);
    }

    /**
     * 将统一消息角色转换为 Spring AI 消息类型。
     */
    private Message toSpringAiMessage(UnifiedChatMessage message) {
        return switch (message.role()) {
            case USER -> new UserMessage(message.content());
            case ASSISTANT -> new AssistantMessage(message.content());
        };
    }

    /**
     * 将统一生成参数转换为 Spring AI ChatOptions。
     */
    private ChatOptions toChatOptions(UnifiedChatRequest request) {
        return ChatOptions.builder()
                .model(model)
                .temperature(request.options().temperature())
                .maxTokens(request.options().maxTokens())
                .topP(request.options().topP())
                .build();
    }

    /**
     * 将单个 Spring AI ChatResponse 转换为统一 MESSAGE 事件。
     */
    private Mono<UnifiedChatStreamEvent> toMessageEvent(
            ChatResponse response,
            AtomicBoolean contentStarted
    ) {
        // 提取当前 chunk 的文本内容。
        String text = extractText(response);

        // 空文本 chunk 不输出给前端。
        if (text == null || text.isEmpty()) {
            return Mono.empty();
        }

        // 一旦输出过文本，就不再允许当前 provider retry。
        contentStarted.set(true);

        return Mono.just(UnifiedChatStreamEvent.message(
                llmProvider,
                model,
                text,
                toMetadata(response)
        ));
    }

    /**
     * 从 Spring AI ChatResponse 中提取文本内容。
     */
    private String extractText(ChatResponse response) {
        if (response == null || response.getResult() == null || response.getResult().getOutput() == null) {
            return "";
        }

        String text = response.getResult().getOutput().getText();
        return text == null ? "" : text;
    }

    /**
     * 从 Spring AI ChatResponse 中提取 token usage。
     */
    private TokenUsage toTokenUsage(ChatResponse response) {
        if (response == null || response.getMetadata() == null || response.getMetadata().getUsage() == null) {
            return TokenUsage.empty();
        }

        var usage = response.getMetadata().getUsage();

        return TokenUsage.of(
                usage.getPromptTokens(),
                usage.getCompletionTokens()
        );
    }

    /**
     * 从 Spring AI ChatResponse 中提取 metadata。
     */
    private Map<String, Object> toMetadata(ChatResponse response) {
        Map<String, Object> metadata = new LinkedHashMap<>();

        // 保存统一 provider 信息。
        put(metadata, "provider", provider);
        put(metadata, "model", model);

        if (response != null && response.getMetadata() != null) {
            // 保留 Spring AI 原始 metadata 字符串，便于排查 provider 行为。
            put(metadata, "springAiMetadata", response.getMetadata().toString());

            if (response.getMetadata().getUsage() != null) {
                var usage = response.getMetadata().getUsage();

                // 保存 token usage 的常用字段。
                put(metadata, "promptTokens", usage.getPromptTokens());
                put(metadata, "completionTokens", usage.getCompletionTokens());
                put(metadata, "totalTokens", usage.getTotalTokens());
            }
        }

        if (response != null && response.getResult() != null && response.getResult().getMetadata() != null) {
            // 保存 generation 级别 metadata，例如 finish reason 等 provider 特有信息。
            put(metadata, "generationMetadata", response.getResult().getMetadata().toString());
        }

        return Map.copyOf(metadata);
    }

    /**
     * 向 metadata 中放入非空字段。
     */
    private void put(Map<String, Object> metadata, String key, Object value) {
        if (value == null) {
            return;
        }

        if (value instanceof String text && text.isBlank()) {
            return;
        }

        metadata.put(key, value);
    }

    /**
     * 合并分阶段返回的 token usage。
     * 新 usage 中非空字段优先，缺失字段保留旧值。
     */
    private TokenUsage mergeUsage(TokenUsage current, TokenUsage incoming) {
        if (incoming == null) {
            return current == null ? TokenUsage.empty() : current;
        }

        Integer inputTokens = incoming.inputTokens() != null
                ? incoming.inputTokens()
                : current == null ? null : current.inputTokens();

        Integer outputTokens = incoming.outputTokens() != null
                ? incoming.outputTokens()
                : current == null ? null : current.outputTokens();

        return TokenUsage.of(inputTokens, outputTokens);
    }

    /**
     * 将 Spring AI / HTTP / Reactor 异常转换为统一 provider 异常。
     */
    private static LlmProviderException toProviderException(String provider, Throwable throwable) {
        Throwable ex = Exceptions.unwrap(throwable);

        // 已经是统一 provider 异常时直接返回。
        if (ex instanceof LlmProviderException providerException) {
            return providerException;
        }

        // WebClient HTTP 错误，通常包含 HTTP 状态码和响应体。
        if (ex instanceof WebClientResponseException webClientResponseException) {
            return new LlmProviderException(
                    provider,
                    webClientResponseException.getStatusCode().value(),
                    "Provider HTTP error",
                    webClientResponseException.getResponseBodyAsString(),
                    webClientResponseException
            );
        }

        // RestClient HTTP 错误，Spring AI 某些底层调用可能使用 RestClient。
        if (ex instanceof RestClientResponseException restClientResponseException) {
            return new LlmProviderException(
                    provider,
                    restClientResponseException.getStatusCode().value(),
                    "Provider HTTP error",
                    restClientResponseException.getResponseBodyAsString(),
                    restClientResponseException
            );
        }

        // Reactor timeout 或 stream idle timeout。
        if (ex instanceof TimeoutException) {
            return new LlmProviderException(
                    provider,
                    -1,
                    "Provider stream timeout",
                    "",
                    ex
            );
        }

        // 网络连接失败、DNS 失败、连接被拒绝等请求级异常。
        if (ex instanceof WebClientRequestException) {
            return new LlmProviderException(
                    provider,
                    -1,
                    "Provider network error",
                    "",
                    ex
            );
        }

        // 其它未知异常统一包装为 provider stream failed。
        return new LlmProviderException(
                provider,
                -1,
                "Provider stream failed",
                "",
                ex
        );
    }

    /**
     * 判断异常是否允许在当前 provider 内部重试。
     */
    private static boolean isRetryable(Throwable throwable) {
        LlmProviderException ex = throwable instanceof LlmProviderException providerException
                ? providerException
                : toProviderException("unknown", throwable);

        int status = ex.statusCode();

        // -1 表示非 HTTP 状态错误；429 / 5xx 通常是临时错误，可以重试。
        return status == -1
                || status == 429
                || status == 500
                || status == 502
                || status == 503
                || status == 504;
    }
}
```
