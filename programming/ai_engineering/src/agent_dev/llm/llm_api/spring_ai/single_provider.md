# 同一个 provider 下切换不同模型

如果想要调用 DashScope 提供的多个不同的模型：

- qwen-plus
- qwen3.7-plus
- qwen-max

可以在调用时覆盖模型参数。

示例：

```java
package com.example.ai;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.openai.OpenAiChatOptions;
import org.springframework.stereotype.Service;

/**
 * 同一个 OpenAI-compatible provider 下的多模型调用服务。
 * 适合 base-url 相同，只是 model 名不同的场景。
 */
@Service
public class QwenModelService {

    private final ChatClient chatClient;

    public QwenModelService(ChatClient.Builder builder) {
        this.chatClient = builder
                .defaultSystem("你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。")
                .build();
    }

    /**
     * 调用指定 Qwen 模型。
     */
    public String chat(String model, String message) {
        return chatClient.prompt()
                .options(OpenAiChatOptions.builder()
                        .model(model)
                        .temperature(0.2)
                        .maxTokens(1000)
                        .build())
                .user(message)
                .call()
                .content();
    }
}
```

调用时：

```java
qwenModelService.chat("qwen3.7-plus", "解释一下 RAG");
qwenModelService.chat("qwen-plus", "解释一下 RAG");
```

这种方式适合：

- 同一个 base-url
- 同一个 api-key
- 同一种 OpenAI-compatible 协议
- 只是模型名不同
