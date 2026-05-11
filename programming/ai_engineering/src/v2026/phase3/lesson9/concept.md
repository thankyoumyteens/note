# 核心概念

## 什么是 ChatClient？

Spring AI 的 `ChatClient` 是一个与 AI Model 通信的 fluent API。官方文档说明，它同时支持同步和流式编程模型，并且可以构建传给模型的 Prompt；Prompt 包含 user message、system message 和模型选项，例如 model、temperature。

你可以把它理解成 Spring AI 提供的高级模型调用客户端。

手写版本：

```java
llmWebClient.post()
        .uri("/v1/chat/completions")
        .bodyValue(request)
        .retrieve()
        .bodyToMono(ChatCompletionResponse.class)
        .block();
```

Spring AI 版本：

```java
chatClient.prompt()
        .system(systemPrompt)
        .user(userPrompt)
        .call()
        .content();
```

它屏蔽了底层 HTTP DTO。

## 什么是 ChatModel？

`ChatModel` 是更底层的模型抽象，`ChatClient` 通常构建在 `ChatModel` 上。

你可以粗略理解：

```text
ChatModel：模型能力接口
ChatClient：更好用的 fluent API
```

本课直接使用 `ChatClient`。
