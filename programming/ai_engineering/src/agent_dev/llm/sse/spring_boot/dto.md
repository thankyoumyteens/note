# 请求 DTO

## 通用请求 DTO

```java
package com.example.ai.dto;

/**
 * 前端 POST SSE 请求。
 * provider 决定使用 qwen / deepseek / openai / claude / qwen-messages。
 */
public record StreamChatRequest(
        String provider,
        String message,
        String system
) {
}
```

```java
package com.example.ai.dto;

/**
 * 标准聊天消息。
 */
public record LlmMessage(
        String role,
        String content
) {
}
```

## OpenAI-compatible 请求 DTO

```java
package com.example.ai.dto.openai;

import com.example.ai.dto.LlmMessage;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * OpenAI-compatible Chat Completions 请求体。
 */
public record OpenAiChatStreamRequest(
        String model,
        List<LlmMessage> messages,
        Double temperature,

        @JsonProperty("max_tokens")
        Integer maxTokens,

        Boolean stream
) {
}
```

## Anthropic Messages 请求 DTO

```java
package com.example.ai.dto.anthropic;

import com.example.ai.dto.LlmMessage;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * Anthropic Messages-compatible 请求体。
 * Claude 原生和 Qwen Anthropic-compatible 都可以复用。
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record AnthropicMessageStreamRequest(
        String model,

        @JsonProperty("max_tokens")
        Integer maxTokens,

        Double temperature,

        String system,

        List<LlmMessage> messages,

        Boolean stream,

        Thinking thinking
) {
    public static Thinking disabledThinking() {
        return new Thinking("disabled");
    }

    public record Thinking(String type) {
    }
}
```
