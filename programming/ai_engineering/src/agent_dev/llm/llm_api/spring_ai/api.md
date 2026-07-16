# 调用 OpenAI-compatible API

## application.yml

```yaml
spring:
  ai:
    model:
      chat: openai

    openai:
      api-key: ${LLM_API_KEY}
      base-url: ${LLM_BASE_URL:https://api.deepseek.com}
      chat:
        completions-path: /chat/completions
        options:
          model: ${LLM_MODEL}
          temperature: 0.2
          max-tokens: 1000
```

## 代码

```java
package com.example.demo;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DemoConsole implements CommandLineRunner {

    private final ChatClient.Builder chatClientBuilder;

    public DemoConsole(ChatClient.Builder chatClientBuilder) {
        this.chatClientBuilder = chatClientBuilder;
    }

    /**
     * 入口
     */
    @Override
    public void run(String... args) {
        ChatClient chatClient = chatClientBuilder
                .defaultSystem("你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。")
                .build();
        String content = chatClient.prompt()
                .user("用一句话解释什么是 RAG。")
                .call()
                .content();
        // 输出大模型的回答
        System.out.println(content);
    }
}
```
