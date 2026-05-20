# 修改 AiChatService

文件：

```text
src/main/java/com/example/aigateway/service/AiChatService.java
```

改成：

```java
package com.example.aigateway.service;

import com.example.aigateway.client.LlmClient;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;

/**
 * AI 聊天业务服务。
 *
 * 负责基础入参校验和调用 LlmClient。
 * 不关心底层到底是 OpenAI、DeepSeek、Qwen 还是其他供应商。
 */
@Service
public class AiChatService {

    private final LlmClient llmClient;

    public AiChatService(LlmClient llmClient) {
        this.llmClient = llmClient;
    }

    /**
     * 普通聊天，一次性返回完整回答。
     */
    public String chat(String message) {
        validateMessage(message);
        return llmClient.chat(message);
    }

    /**
     * 流式聊天，返回多个文本片段。
     */
    public Flux<String> streamChat(String message) {
        validateMessage(message);
        return llmClient.streamChat(message);
    }

    /**
     * 统一校验用户输入。
     */
    private void validateMessage(String message) {
        if (message == null || message.isBlank()) {
            throw new IllegalArgumentException("message cannot be empty");
        }
    }
}
```
