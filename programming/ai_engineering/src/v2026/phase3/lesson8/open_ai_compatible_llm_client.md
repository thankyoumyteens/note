# 修改 OpenAiCompatibleLlmClient

## 修改 OpenAiCompatibleLlmClient 构造器

注入限流器：

```java
private final LlmRateLimiter llmRateLimiter;
```

构造器增加参数：

```java
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
```

需要 import：

```java
import com.example.aigateway.service.LlmRateLimiter;
import com.example.aigateway.exception.LlmFallbackException;
import com.example.aigateway.exception.LlmRateLimitException;
```

## 抽取一次真实模型调用

在 `OpenAiCompatibleLlmClient` 中新增私有方法：

```java
private ChatCompletionResponse doChatCompletion(ChatCompletionRequest request) {
    return llmWebClient.post()
            .uri("/v1/chat/completions")
            .bodyValue(request)
            .retrieve()
            .bodyToMono(ChatCompletionResponse.class)
            .block();
}
```

这样 `complete()` 中更容易做重试。

## 判断是否可重试

新增：

```java
private boolean isRetryable(Throwable e) {
    if (e instanceof org.springframework.web.reactive.function.client.WebClientResponseException responseException) {
        int status = responseException.getStatusCode().value();
        return status == 500 || status == 502 || status == 503 || status == 504 || status == 429;
    }

    return e instanceof java.util.concurrent.TimeoutException
            || e instanceof java.net.ConnectException
            || e instanceof java.io.IOException;
}
```

注意：部分 WebClient 超时异常不一定直接是 `TimeoutException`，可能被包装。
当前先做基础判断，后续再完善错误分类。

## 改造 complete 方法

把 `complete(systemPrompt, userPrompt, callType)` 改成这个结构。

```java
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

            boolean retryable = isRetryable(e);

            if (!retryable || attempt == maxAttempts) {
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
```

## 新增重试等待方法

```java
private void sleepBeforeRetry(int attempt) {
    try {
        Thread.sleep(300L * attempt);
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        throw new RuntimeException("Retry interrupted", e);
    }
}
```

当前是简单线性等待：

```text
第 1 次失败后等待 300ms
```

后续可以升级为：

```text
指数退避 exponential backoff
随机抖动 jitter
```

## 修改 streamChat 加限流

在 `streamChat` 开头加：

```java
llmRateLimiter.acquire();
```

## 本课暂不处理 streamChat 的复杂 fallback

流式调用一旦开始返回，fallback 会更复杂。

本课只给 `streamChat` 增加限流失败处理，不做完整重试。

原因：

```text
流式响应可能已经部分返回，重试会造成重复内容。
```
