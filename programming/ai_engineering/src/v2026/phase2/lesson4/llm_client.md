# 扩展 LlmClient

当前你的 `LlmClient` 应该类似：

```java
public interface LlmClient {

    String chat(String message);

    Flux<String> streamChat(String message);
}
```

改成：

```java
package com.example.aigateway.client;

import reactor.core.publisher.Flux;

public interface LlmClient {

    String chat(String message);

    Flux<String> streamChat(String message);

    String complete(String systemPrompt, String userPrompt);
}
```

新增：

```java
String complete(String systemPrompt, String userPrompt);
```

为什么要加这个方法？

因为后面很多业务不是单纯聊天，而是：

```text
systemPrompt：定义任务、规则、输出格式
userPrompt：用户输入或业务文本
```

例如：

```text
systemPrompt = 你是一个任务信息抽取器，只能输出 JSON
userPrompt = 明天下午三点提醒我给张三发报价单，优先级高。
```
