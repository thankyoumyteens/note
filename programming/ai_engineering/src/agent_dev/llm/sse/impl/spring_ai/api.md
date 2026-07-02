# 调用 OpenAI-compatible API

Spring AI 的 ChatClient 本身支持同步调用和流式调用；同步用 `.call()`，流式用 `.stream()`。

## application.yml

```yaml
spring:
  ai:
    model:
      chat: openai

    openai:
      api-key: 换成你自己的KEY
      base-url: https://api.deepseek.com
      chat:
        completions-path: /chat/completions
        options:
          model: deepseek-v4-pro
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

        // stream() 会返回流式响应，content() 会把模型输出转换成 Flux<String>。
        Flux<String> contentFlux = chatClient.prompt()
                .user("用一句话解释什么是 RAG。")
                .stream()
                .content();

        // CommandLineRunner 里必须阻塞等待流结束，否则应用可能提前退出。
        contentFlux
                .doOnNext(System.out::print)
                .doOnComplete(() -> System.out.println("\n--- stream finished ---"))
                .blockLast();
    }
}
```
