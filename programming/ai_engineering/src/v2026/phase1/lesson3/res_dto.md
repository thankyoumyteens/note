# 增加流式响应 DTO

普通模型响应是完整 JSON，例如：

```json
{
  "choices": [
    {
      "message": {
        "content": "RAG 是一种..."
      }
    }
  ]
}
```

流式响应是一段段 chunk，例如：

```text
data: {"choices":[{"delta":{"content":"RAG"}}]}

data: {"choices":[{"delta":{"content":" 是"}}]}

data: {"choices":[{"delta":{"content":"一种"}}]}

data: [DONE]
```

每个 chunk 只包含新增内容。

所以不能再读取：

```text
message.content
```

而是要读取：

```text
delta.content
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

/**
 * OpenAI-compatible streaming chunk DTO。
 *
 * 普通响应使用 ChatCompletionResponse，其中内容在 message.content。
 * 流式响应使用 ChatCompletionChunk，其中新增内容在 delta.content。
 */
public record ChatCompletionChunk(
        List<Choice> choices
) {
    public record Choice(
            Delta delta,
            String finish_reason
    ) {
    }

    /**
     * delta 表示本次 chunk 新增的内容。
     *
     * 常见字段：
     * - role：有些供应商会在第一个 chunk 返回 assistant role
     * - content：本次新增文本片段
     */
    public record Delta(
            String role,
            String content
    ) {
    }
}
```
