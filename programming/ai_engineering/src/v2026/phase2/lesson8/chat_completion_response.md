# 修改 ChatCompletionResponse

确认你的 response DTO 中包含 usage：

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
            Integer prompt_tokens,
            Integer completion_tokens,
            Integer total_tokens
    ) {
    }
}
```
