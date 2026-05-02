# 增加流式响应 DTO

OpenAI-compatible 的流式返回不是完整 JSON，而是一行一行的：

```text
data: {"choices":[{"delta":{"content":"RAG"}}]}
data: {"choices":[{"delta":{"content":" 是"}}]}
data: {"choices":[{"delta":{"content":"一种"}}]}
data: [DONE]
```

所以我们需要一个流式响应 DTO。

新建：

```text
client.openai.dto/ChatCompletionChunk.java
```

代码：

```java
package com.example.aigateway.client.openai.dto;

import java.util.List;

public record ChatCompletionChunk(
        List<Choice> choices
) {
    public record Choice(
            Delta delta,
            String finish_reason
    ) {
    }

    public record Delta(
            String role,
            String content
    ) {
    }
}
```
