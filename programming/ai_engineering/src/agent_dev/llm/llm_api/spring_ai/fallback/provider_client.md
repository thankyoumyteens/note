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
import com.example.llm.exceptions.LlmProviderException;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.messages.Message;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.chat.model.ChatResponse;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.concurrent.ExecutorService;
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

        return new UnifiedChatResponse(
                llmProvider,
                model,
                content,
                null,
                TokenUsage.empty(),
                Map.of(
                        "springAiMetadata", response == null || response.getMetadata() == null
                                ? ""
                                : response.getMetadata().toString()
                )
        );
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
        long millis = switch (attempt) {
            case 0 -> 500L;
            case 1 -> 1000L;
            default -> 2000L;
        };

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
