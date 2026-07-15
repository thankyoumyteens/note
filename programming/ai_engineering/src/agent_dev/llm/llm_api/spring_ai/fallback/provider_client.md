# SpringAiProviderClient

这是核心类：实现 timeout + retry + Spring AI 调用 + 异常归一化，openaiChatClient、deepseekChatClient 等 bean 都会通过它调用大模型接口。

```java
package com.example.llm.provider;

import com.example.llm.dto.ChatRole;
import com.example.llm.dto.LlmProvider;
import com.example.llm.dto.TokenUsage;
import com.example.llm.dto.UnifiedChatMessage;
import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatResponse;
import com.example.llm.dto.UnifiedStopReason;
import com.example.llm.exceptions.LlmProviderException;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.messages.Message;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.metadata.EmptyUsage;
import org.springframework.ai.chat.metadata.Usage;
import org.springframework.ai.chat.model.ChatResponse;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/**
 * Spring AI provider client。
 * 每个实例绑定一个 provider 对应的 ChatClient。
 */
public class SpringAiProviderClient implements LlmProviderClient {

    private final String provider;
    private final LlmProvider llmProvider;
    private final String model;
    private final ChatClient chatClient;
    private final Duration requestTimeout;
    private final int maxRetries;
    private final ExecutorService executorService;

    public SpringAiProviderClient(
            String provider,
            LlmProvider llmProvider,
            String model,
            ChatClient chatClient,
            Duration requestTimeout,
            int maxRetries,
            ExecutorService executorService
    ) {
        this.provider = provider;
        this.llmProvider = llmProvider;
        this.model = model;
        this.chatClient = chatClient;
        this.requestTimeout = requestTimeout;
        this.maxRetries = maxRetries;
        this.executorService = executorService;
    }

    @Override
    public String provider() {
        return provider;
    }

    @Override
    public UnifiedChatResponse chat(UnifiedChatRequest request) {
        LlmProviderException lastException = null;

        for (int attempt = 0; attempt <= maxRetries; attempt++) {
            try {
                return callOnceWithTimeout(request);

            } catch (RuntimeException ex) {
                LlmProviderException providerException = toProviderException(unwrap(ex));
                lastException = providerException;

                if (!isRetryable(providerException) || attempt == maxRetries) {
                    throw providerException;
                }

                sleepBeforeNextRetry(attempt);
            }
        }

        throw lastException == null
                ? new LlmProviderException(provider, -1, "Provider call failed", "", null)
                : lastException;
    }

    private UnifiedChatResponse callOnceWithTimeout(UnifiedChatRequest request) {
        try {
            // 单次 provider 尝试的请求级总超时。
            return CompletableFuture
                    .supplyAsync(() -> doChat(request), executorService)
                    .orTimeout(requestTimeout.toMillis(), TimeUnit.MILLISECONDS)
                    .join();

        } catch (CompletionException ex) {
            throw ex;
        }
    }

    private UnifiedChatResponse doChat(UnifiedChatRequest request) {
        ChatResponse response = chatClient.prompt()
                .messages(toSpringMessages(request))
                .call()
                .chatResponse();

        String content = extractContent(response);
        String rawStopReason = extractStopReason(response);

        return new UnifiedChatResponse(
                llmProvider,
                model,
                content,
                toStopReason(rawStopReason),
                toTokenUsage(response),
                Map.of(
                        "rawStopReason", rawStopReason == null ? "" : rawStopReason,
                        "springAiMetadata", response == null || response.getMetadata() == null
                                ? ""
                                : response.getMetadata().toString()
                )
        );
    }

    private String extractStopReason(ChatResponse response) {
        if (response == null
                || response.getResult() == null
                || response.getResult().getMetadata() == null
                || response.getResult().getMetadata().getFinishReason() == null
                || response.getResult().getMetadata().getFinishReason().isBlank()) {
            return null;
        }

        return response.getResult().getMetadata().getFinishReason();
    }

    private UnifiedStopReason toStopReason(String reason) {
        if (reason == null) {
            return null;
        }

        return switch (reason.toLowerCase(Locale.ROOT)) {
            case "stop" -> UnifiedStopReason.STOP;
            case "length" -> UnifiedStopReason.LENGTH;
            case "tool_calls", "function_call" -> UnifiedStopReason.TOOL_CALLS;
            case "content_filter" -> UnifiedStopReason.CONTENT_FILTER;
            default -> UnifiedStopReason.OTHER;
        };
    }

    /**
     * 从 Spring AI ChatResponse metadata 提取统一 Token 用量。
     */
    private TokenUsage toTokenUsage(ChatResponse response) {
        if (response == null || response.getMetadata() == null) {
            return TokenUsage.empty();
        }

        Usage usage = response.getMetadata().getUsage();

        // EmptyUsage 表示 Provider 没有返回 usage，不能当成真实的零 Token。
        if (usage == null || usage instanceof EmptyUsage) {
            return TokenUsage.empty();
        }

        Integer inputTokens = usage.getPromptTokens();
        Integer outputTokens = usage.getCompletionTokens();
        Integer totalTokens = usage.getTotalTokens();

        if (totalTokens == null && inputTokens != null && outputTokens != null) {
            totalTokens = inputTokens + outputTokens;
        }

        return new TokenUsage(inputTokens, outputTokens, totalTokens);
    }

    private List<Message> toSpringMessages(UnifiedChatRequest request) {
        List<Message> messages = new ArrayList<>();

        if (request.system() != null && !request.system().isBlank()) {
            messages.add(new SystemMessage(request.system()));
        }

        for (UnifiedChatMessage message : request.messages()) {
            messages.add(toSpringMessage(message));
        }

        return messages;
    }

    private Message toSpringMessage(UnifiedChatMessage message) {
        if (message.role() == ChatRole.USER) {
            return new UserMessage(message.content());
        }

        if (message.role() == ChatRole.ASSISTANT) {
            return new AssistantMessage(message.content());
        }

        throw new IllegalArgumentException("Unsupported chat role: " + message.role());
    }

    private String extractContent(ChatResponse response) {
        if (response == null
                || response.getResult() == null
                || response.getResult().getOutput() == null
                || response.getResult().getOutput().getText() == null) {
            return "";
        }

        return response.getResult().getOutput().getText();
    }

    private LlmProviderException toProviderException(Throwable ex) {
        if (ex instanceof LlmProviderException providerException) {
            return providerException;
        }

        if (ex instanceof TimeoutException) {
            return new LlmProviderException(
                    provider,
                    -1,
                    "Provider request timeout",
                    "",
                    ex
            );
        }

        Integer statusCode = SpringAiExceptionUtils.findHttpStatusCode(ex);
        String responseBody = SpringAiExceptionUtils.findResponseBody(ex);

        if (statusCode != null) {
            return new LlmProviderException(
                    provider,
                    statusCode,
                    "Spring AI provider HTTP call failed",
                    responseBody,
                    ex
            );
        }

        if (SpringAiExceptionUtils.isNetworkError(ex)) {
            return new LlmProviderException(
                    provider,
                    -1,
                    "Provider network error",
                    "",
                    ex
            );
        }

        return new LlmProviderException(
                provider,
                -1,
                "Spring AI provider call failed",
                "",
                ex
        );
    }

    private boolean isRetryable(LlmProviderException ex) {
        int status = ex.statusCode();

        return status == -1
                || status == 429
                || status == 500
                || status == 502
                || status == 503
                || status == 504;
    }

    private void sleepBeforeNextRetry(int attempt) {
        long baseMillis = Math.min(500L << Math.min(attempt, 3), 3000L);
        long millis = (long) (baseMillis * ThreadLocalRandom.current().nextDouble(0.8, 1.2));

        try {
            Thread.sleep(millis);
        } catch (InterruptedException ex) {
            Thread.currentThread().interrupt();
            throw new LlmProviderException(
                    provider,
                    -1,
                    "Retry sleep interrupted",
                    "",
                    ex
            );
        }
    }

    private Throwable unwrap(Throwable ex) {
        Throwable current = ex;

        while (current instanceof CompletionException && current.getCause() != null) {
            current = current.getCause();
        }

        return current;
    }
}
```

## 与另外两种实现的区别

- WebClient 从 Provider 原始 JSON 的 `usage` 字段映射 Token。
- Spring AI 从 generation metadata 读取停止原因，从 response metadata 读取 `Usage`。
- Python SDK 从响应对象的 `usage` 属性映射 Token。

三种实现最终都转换为统一 `TokenUsage`；Provider 未返回 usage 时字段为 `null`，真实零 Token 保留为 `0`。
