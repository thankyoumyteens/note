# 创建 OpenAI-compatible DTO

新建包：

```text
client.openai.dto
```

## ChatCompletionRequest

```java
package com.example.aigateway.client.openai.dto;

import java.util.List;

public record ChatCompletionRequest(
        String model,
        List<Message> messages,
        Double temperature
) {
    public record Message(
            String role,
            String content
    ) {
    }
}
```

## ChatCompletionResponse

```java
package com.example.aigateway.client.openai.dto;

import java.util.List;

public record ChatCompletionResponse(
        List<Choice> choices,
        Usage usage
) {
    public record Choice(
            int index,
            Message message,
            String finish_reason
    ) {
    }

    public record Message(
            String role,
            String content
    ) {
    }

    public record Usage(
            int prompt_tokens,
            int completion_tokens,
            int total_tokens
    ) {
    }
}
```

这里用的是传统 OpenAI-compatible `/v1/chat/completions` 格式。

官方新项目也可以优先看 Responses API，但兼容生态里 `chat/completions` 仍然很常见。OpenAI 官方迁移文档也说明 Chat Completions 仍被支持，而 Responses API 是较新的推荐方向。
