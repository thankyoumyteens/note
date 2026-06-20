# 调用 Anthropic Messages API

## application.yml

下面按 **Spring AI 1.1.x** 写法给出，和你前面 OpenAI-compatible 的配置风格一致：

```yaml
spring:
  ai:
    model:
      chat: anthropic

    anthropic:
      api-key: 换成你自己的KEY
      base-url: https://api.anthropic.com
      version: 2023-06-01
      chat:
        options:
          model: claude-sonnet-4-20250514
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
