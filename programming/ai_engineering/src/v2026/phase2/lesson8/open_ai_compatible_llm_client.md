# 修改 OpenAiCompatibleLlmClient

核心改动：

```text
1. 注入 LlmCallLogService
2. 注入 LlmRateLimiter
3. complete 支持 callType
4. 记录 success / failure
5. 记录 latency
6. 记录 token usage
7. 增加简单重试
8. 增加 fallback 异常
```

关键代码结构如下，你可以按这个替换或合并：

```java
package com.example.aigateway.client.openai;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.client.openai.dto.ChatCompletionChunk;
import com.example.aigateway.client.openai.dto.ChatCompletionRequest;
import com.example.aigateway.client.openai.dto.ChatCompletionResponse;
import com.example.aigateway.config.LlmProperties;
import com.example.aigateway.dto.LlmCallType;
import com.example.aigateway.exception.LlmFallbackException;
import com.example.aigateway.service.LlmCallLogService;
import com.example.aigateway.service.LlmRateLimiter;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.net.ConnectException;
import java.util.List;
import java.util.concurrent.TimeoutException;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import reactor.core.publisher.Flux;

@Component
public class OpenAiCompatibleLlmClient implements LlmClient {

    private final WebClient llmWebClient;
    private final LlmProperties properties;
    private final ObjectMapper objectMapper;
    private final LlmCallLogService llmCallLogService;
    private final LlmRateLimiter llmRateLimiter;

    public OpenAiCompatibleLlmClient(
            WebClient llmWebClient,
            LlmProperties properties,
            ObjectMapper objectMapper,
            LlmCallLogService llmCallLogService,
            LlmRateLimiter llmRateLimiter
    ) {
        this.llmWebClient = llmWebClient;
        this.properties = properties;
        this.objectMapper = objectMapper;
        this.llmCallLogService = llmCallLogService;
        this.llmRateLimiter = llmRateLimiter;
    }

    @Override
    public String chat(String message) {
        return complete(
                "你是一个严谨、简洁的 AI 应用开发助手。",
                message,
                LlmCallType.CHAT
        );
    }

    @Override
    public String complete(String systemPrompt, String userPrompt, LlmCallType callType) {
        llmRateLimiter.acquire();

        long start = System.currentTimeMillis();

        ChatCompletionRequest request = new ChatCompletionRequest(
                properties.getModel(),
                List.of(
                        new ChatCompletionRequest.Message("system", systemPrompt),
                        new ChatCompletionRequest.Message("user", userPrompt)
                ),
                0.1,
                false
        );

        int maxAttempts = 2;
        Throwable lastError = null;

        for (int attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                ChatCompletionResponse response = doChatCompletion(request);

                long latencyMs = System.currentTimeMillis() - start;

                if (response == null || response.choices() == null || response.choices().isEmpty()) {
                    throw new IllegalStateException("LLM response is empty");
                }

                ChatCompletionResponse.Choice firstChoice = response.choices().get(0);

                if (firstChoice.message() == null || firstChoice.message().content() == null) {
                    throw new IllegalStateException("LLM response message is empty");
                }

                ChatCompletionResponse.Usage usage = response.usage();

                llmCallLogService.recordSuccess(
                        callType,
                        properties.getModel(),
                        latencyMs,
                        usage == null ? null : usage.prompt_tokens(),
                        usage == null ? null : usage.completion_tokens(),
                        usage == null ? null : usage.total_tokens()
                );

                return firstChoice.message().content().strip();

            } catch (Exception e) {
                lastError = e;

                if (!isRetryable(e) || attempt == maxAttempts) {
                    long latencyMs = System.currentTimeMillis() - start;

                    llmCallLogService.recordFailure(
                            callType,
                            properties.getModel(),
                            latencyMs,
                            e.getMessage()
                    );

                    throw new LlmFallbackException(
                            "LLM provider is temporarily unavailable. Please try again later.",
                            e
                    );
                }

                sleepBeforeRetry(attempt);
            }
        }

        throw new LlmFallbackException(
                "LLM provider is temporarily unavailable. Please try again later.",
                lastError
        );
    }

    @Override
    public Flux<String> streamChat(String message) {
        llmRateLimiter.acquire();

        long start = System.currentTimeMillis();

        ChatCompletionRequest request = new ChatCompletionRequest(
                properties.getModel(),
                List.of(
                        new ChatCompletionRequest.Message(
                                "system",
                                "你是一个严谨、简洁的 AI 应用开发助手。"
                        ),
                        new ChatCompletionRequest.Message("user", message)
                ),
                0.3,
                true
        );

        return llmWebClient.post()
                .uri("/v1/chat/completions")
                .accept(MediaType.TEXT_EVENT_STREAM)
                .bodyValue(request)
                .retrieve()
                .bodyToFlux(String.class)
                .flatMap(this::parseSseChunk)
                .doOnComplete(() -> llmCallLogService.recordSuccess(
                        LlmCallType.STREAM_CHAT,
                        properties.getModel(),
                        System.currentTimeMillis() - start,
                        null,
                        null,
                        null
                ))
                .doOnError(e -> llmCallLogService.recordFailure(
                        LlmCallType.STREAM_CHAT,
                        properties.getModel(),
                        System.currentTimeMillis() - start,
                        e.getMessage()
                ))
                .onErrorResume(e -> Flux.just("[ERROR] " + e.getMessage()));
    }

    private ChatCompletionResponse doChatCompletion(ChatCompletionRequest request) {
        return llmWebClient.post()
                .uri("/v1/chat/completions")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(ChatCompletionResponse.class)
                .block();
    }

    private boolean isRetryable(Throwable e) {
        if (e instanceof WebClientResponseException responseException) {
            int status = responseException.getStatusCode().value();
            return status == 429 || status == 500 || status == 502 || status == 503 || status == 504;
        }

        return e instanceof TimeoutException
                || e instanceof ConnectException
                || e instanceof IOException;
    }

    private void sleepBeforeRetry(int attempt) {
        try {
            Thread.sleep(300L * attempt);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new RuntimeException("Retry interrupted", e);
        }
    }

    private Flux<String> parseSseChunk(String rawChunk) {
        try {
            if (rawChunk == null || rawChunk.isBlank()) {
                return Flux.empty();
            }

            String text = rawChunk.strip();

            if ("[DONE]".equals(text) || "data: [DONE]".equals(text)) {
                return Flux.empty();
            }

            if (text.startsWith("data:")) {
                text = text.substring("data:".length()).strip();
            }

            if (text.isBlank() || "[DONE]".equals(text)) {
                return Flux.empty();
            }

            ChatCompletionChunk chunk = objectMapper.readValue(text, ChatCompletionChunk.class);

            if (chunk.choices() == null || chunk.choices().isEmpty()) {
                return Flux.empty();
            }

            ChatCompletionChunk.Choice choice = chunk.choices().get(0);

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
