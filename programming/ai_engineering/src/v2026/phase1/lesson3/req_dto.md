# 增加流式请求 DTO

OpenAI-compatible Chat Completions 要启用 streaming，通常需要在请求中增加：

```json
{
  "stream": true
}
```

你现在已经有普通请求 DTO：

```java
ChatCompletionRequest
```

它没有 `stream` 字段。

我们先直接改它，增加一个 `Boolean stream` 字段。

```java
package com.example.aigateway.client.openai.dto;

import java.util.List;

/**
 * OpenAI-compatible Chat Completions 请求 DTO。
 *
 * 本 DTO 同时用于普通非流式调用和流式调用。
 *
 * stream:
 * - false：模型完整生成后一次性返回
 * - true：模型边生成边返回 streaming chunks
 */
public record ChatCompletionRequest(
        String model,
        List<Message> messages,
        Double temperature,
        Boolean stream
) {
    /**
     * Chat Completions 的消息结构。
     *
     * role 常见取值：
     * - system：系统级约束
     * - user：用户输入
     * - assistant：模型历史回答
     */
    public record Message(
            String role,
            String content
    ) {
    }
}
```

然后你原来的非流式调用需要多传一个 `false`。

原来：

```java
ChatCompletionRequest request = new ChatCompletionRequest(
        properties.getModel(),
        List.of(...),
        0.3
);
```

改成：

```java
ChatCompletionRequest request = new ChatCompletionRequest(
        properties.getModel(),
        List.of(...),
        0.3,
        false
);
```

流式调用时传：

```java
true
```
