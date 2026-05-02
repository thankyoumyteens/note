# 增加流式请求 DTO

你现在已经有普通请求 DTO：

```java
ChatCompletionRequest
```

它没有 `stream` 字段。

我们先直接改它，增加一个 `Boolean stream` 字段。

```java
package com.example.aigateway.client.openai.dto;

import java.util.List;

public record ChatCompletionRequest(
        String model,
        List<Message> messages,
        Double temperature,
        Boolean stream
) {
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
