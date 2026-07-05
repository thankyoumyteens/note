# 调用 Anthropic Messages API

## application.yml

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
import reactor.core.publisher.Flux;

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

        // stream() 启用流式调用，content() 返回 Flux<String>。
        Flux<String> contentFlux = chatClient.prompt()
                .user("用一句话解释什么是 RAG。")
                .stream()
                .content();

        // CommandLineRunner 中需要阻塞等待流结束，否则程序可能提前退出。
        contentFlux
                .doOnNext(System.out::print)
                .doOnComplete(() -> System.out.println("\n--- stream finished ---"))
                .blockLast();
    }
}
```
