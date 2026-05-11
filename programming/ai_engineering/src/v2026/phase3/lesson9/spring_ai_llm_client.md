# 新增 SpringAiLlmClient

新建包：

```text
client.springai
```

新建：

```text
client.springai/SpringAiLlmClient.java
```

代码：

```java
package com.example.aigateway.client.springai;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.dto.LlmCallType;
import com.example.aigateway.service.LlmCallLogService;
import com.example.aigateway.service.LlmRateLimiter;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Flux;

@Component
@ConditionalOnProperty(
        name = "llm.provider",
        havingValue = "spring-ai"
)
public class SpringAiLlmClient implements LlmClient {

    private final ChatClient chatClient;
    private final LlmCallLogService llmCallLogService;
    private final LlmRateLimiter llmRateLimiter;

    public SpringAiLlmClient(
            ChatClient.Builder chatClientBuilder,
            LlmCallLogService llmCallLogService,
            LlmRateLimiter llmRateLimiter
    ) {
        this.chatClient = chatClientBuilder.build();
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
    public Flux<String> streamChat(String message) {
        throw new UnsupportedOperationException("SpringAiLlmClient streamChat is not implemented in this lesson");
    }

    @Override
    public String complete(String systemPrompt, String userPrompt, LlmCallType callType) {
        llmRateLimiter.acquire();

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
                    "spring-ai-configured-model",
                    latencyMs,
                    null,
                    null,
                    null
            );

            return content == null ? "" : content.strip();

        } catch (Exception e) {
            long latencyMs = System.currentTimeMillis() - start;

            llmCallLogService.recordFailure(
                    callType,
                    "spring-ai-configured-model",
                    latencyMs,
                    e.getMessage()
            );

            throw e;
        }
    }
}
```

说明：

```text
这里 token usage 暂时记为 null。
```

原因是本课只验证 Spring AI 基础 ChatClient 接入，不处理 usage 提取。
后续如果继续 Spring AI 路线，再补 usage、streaming、tool calling 和 observation。
