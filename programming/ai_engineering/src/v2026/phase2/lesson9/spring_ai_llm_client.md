# 新增 SpringAiLlmClient

新增一个基于 Spring AI 的 `LlmClient` 实现，但不让业务层感知 Spring AI。

Spring AI 的 `ChatClient` 是调用模型的 Fluent API。官方示例中可以通过 `ChatClient.Builder` 构建 `ChatClient`，然后调用 `chatClient.prompt(...).call().content()` 获取模型响应。

但在我们的架构里，`ChatClient` 只能出现在：

```text
SpringAiLlmClient 内部
```

不能出现在：

```text
Controller
AiChatService
TaskExtractionService
OrderAssistantService
```

#### 代码

新建文件：

```text
src/main/java/com/example/aigateway/client/springai/SpringAiLlmClient.java
```

代码：

```java
package com.example.aigateway.client.springai;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.config.LlmProperties;
import com.example.aigateway.dto.LlmCallType;
import com.example.aigateway.dto.RateLimitRequest;
import com.example.aigateway.dto.RateLimitResult;
import com.example.aigateway.exception.LlmFallbackException;
import com.example.aigateway.exception.LlmRateLimitException;
import com.example.aigateway.service.DistributedRateLimiter;
import com.example.aigateway.service.LlmCallLogService;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Flux;

/**
 * 基于 Spring AI 的 LlmClient 实现。
 *
 * 注意：
 * - Spring AI 只作为 LlmClient 的一种底层实现
 * - Controller / Service 仍然只依赖 LlmClient
 * - 不允许业务层直接依赖 ChatClient
 */
@Component
@ConditionalOnProperty(
        name = "llm.provider",
        havingValue = "spring-ai"
)
public class SpringAiLlmClient implements LlmClient {

    private final ChatClient chatClient;
    private final LlmProperties properties;
    private final LlmCallLogService llmCallLogService;
    private final DistributedRateLimiter distributedRateLimiter;

    public SpringAiLlmClient(
            ChatClient.Builder chatClientBuilder,
            LlmProperties properties,
            LlmCallLogService llmCallLogService,
            DistributedRateLimiter distributedRateLimiter
    ) {
        this.chatClient = chatClientBuilder.build();
        this.properties = properties;
        this.llmCallLogService = llmCallLogService;
        this.distributedRateLimiter = distributedRateLimiter;
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
    public Flux<String> streamChat(String message) {
        acquireRateLimit(LlmCallType.STREAM_CHAT);

        long start = System.currentTimeMillis();

        try {
            return chatClient.prompt()
                    .system("你是一个严谨、简洁的 AI 应用开发助手。")
                    .user(message)
                    .stream()
                    .content()
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
                    ));

        } catch (Exception e) {
            llmCallLogService.recordFailure(
                    LlmCallType.STREAM_CHAT,
                    properties.getModel(),
                    System.currentTimeMillis() - start,
                    e.getMessage()
            );

            return Flux.error(new LlmFallbackException(
                    "Spring AI provider is temporarily unavailable. Please try again later.",
                    e
            ));
        }
    }

    @Override
    public String complete(
            String systemPrompt,
            String userPrompt,
            LlmCallType callType
    ) {
        acquireRateLimit(callType);

        long start = System.currentTimeMillis();

        try {
            String content = chatClient.prompt()
                    .system(systemPrompt)
                    .user(userPrompt)
                    .call()
                    .content();

            long latencyMs = System.currentTimeMillis() - start;

            llmCallLogService.recordSuccess(
                    callType,
                    properties.getModel(),
                    latencyMs,
                    null,
                    null,
                    null
            );

            if (content == null || content.isBlank()) {
                throw new IllegalStateException("Spring AI response content is empty");
            }

            return content.strip();

        } catch (Exception e) {
            long latencyMs = System.currentTimeMillis() - start;

            llmCallLogService.recordFailure(
                    callType,
                    properties.getModel(),
                    latencyMs,
                    e.getMessage()
            );

            throw new LlmFallbackException(
                    "Spring AI provider is temporarily unavailable. Please try again later.",
                    e
            );
        }
    }

    /**
     * 保持第 8.5 课的分布式限流能力。
     *
     * 即使底层换成 Spring AI，也不能绕过 AI Gateway 的治理层。
     */
    private void acquireRateLimit(LlmCallType callType) {
        RateLimitResult result = distributedRateLimiter.acquire(
                RateLimitRequest.forLlmCall(
                        callType,
                        properties.getModel()
                )
        );

        if (!result.allowed()) {
            throw new LlmRateLimitException(
                    "Too many LLM requests. Please try again later.",
                    result.key(),
                    result.current(),
                    result.limit(),
                    result.ttlSeconds()
            );
        }
    }
}
```

#### 代码说明

这个类重点不是“能调用模型”，而是证明：

```text
Spring AI 可以接进来，但不能绕过 LlmClient
Spring AI 可以接进来，但不能绕过限流
Spring AI 可以接进来，但不能绕过调用日志
Spring AI 可以接进来，但不能绕过 fallback
```

当前 `recordSuccess` 里的 token usage 写成 `null`，因为 Spring AI 的 token usage 提取方式和具体版本 / 模型响应有关。本课先不深挖，后续 LLMOps 或 Spring AI Observability 再处理。
