# 统一 DTO

## 枚举

```java
package com.example.llm.dto;

public enum LlmProvider {
    OPENAI,
    DEEPSEEK,
    ANTHROPIC
}
```

```java
package com.example.llm.dto;

public enum ChatRole {
    USER,
    ASSISTANT
}
```

## 统一消息：UnifiedChatMessage

```java
package com.example.llm.dto;

/**
 * 统一聊天消息。
 * system 不放在这里，单独放在 UnifiedChatRequest.system。
 */
public record UnifiedChatMessage(
        ChatRole role,
        String content
) {

    public UnifiedChatMessage {
        if (role == null) {
            throw new IllegalArgumentException("role must not be null");
        }

        if (content == null || content.isBlank()) {
            throw new IllegalArgumentException("content must not be blank");
        }
    }

    public static UnifiedChatMessage user(String content) {
        return new UnifiedChatMessage(ChatRole.USER, content);
    }

    public static UnifiedChatMessage assistant(String content) {
        return new UnifiedChatMessage(ChatRole.ASSISTANT, content);
    }
}
```

## 生成参数：LlmGenerationOptions

```java
package com.example.llm.dto;

/**
 * 统一生成参数。
 * ProviderClient 可按需映射到具体模型参数。
 */
public record LlmGenerationOptions(
        Double temperature,
        Integer maxTokens,
        Double topP
) {

    public static LlmGenerationOptions defaultOptions() {
        return new LlmGenerationOptions(0.2, 1000, null);
    }
}
```

## 统一请求：UnifiedChatRequest

```java
package com.example.llm.dto;

import java.util.List;
import java.util.Map;

/**
 * 统一聊天请求。
 * provider 不放在请求里，由 ProviderFallbackRouter 决定调用顺序。
 */
public record UnifiedChatRequest(
        String system,
        List<UnifiedChatMessage> messages,
        LlmGenerationOptions options,
        Map<String, Object> metadata
) {

    public UnifiedChatRequest {
        messages = messages == null ? List.of() : List.copyOf(messages);
        metadata = metadata == null ? Map.of() : Map.copyOf(metadata);
        options = options == null ? LlmGenerationOptions.defaultOptions() : options;

        if (messages.isEmpty()) {
            throw new IllegalArgumentException("messages must not be empty");
        }
    }

    public static UnifiedChatRequest of(String system, String userMessage) {
        return new UnifiedChatRequest(
                system,
                List.of(UnifiedChatMessage.user(userMessage)),
                LlmGenerationOptions.defaultOptions(),
                Map.of()
        );
    }
}
```

## Token 用量：TokenUsage

```java
package com.example.llm.dto;

/**
 * 统一 token usage。
 * 如果暂时无法从 Spring AI metadata 中稳定提取，则返回 empty。
 */
public record TokenUsage(
        Integer inputTokens,
        Integer outputTokens,
        Integer totalTokens
) {

    public static TokenUsage empty() {
        return new TokenUsage(null, null, null);
    }

    public static TokenUsage of(Integer inputTokens, Integer outputTokens) {
        Integer total = null;

        if (inputTokens != null && outputTokens != null) {
            total = inputTokens + outputTokens;
        }

        return new TokenUsage(inputTokens, outputTokens, total);
    }
}
```

## 统一响应：UnifiedChatResponse

```java
package com.example.llm.dto;

import java.util.Map;

/**
 * 统一聊天响应。
 * provider 表示实际命中的 provider。
 */
public record UnifiedChatResponse(
        LlmProvider provider,
        String model,
        String content,
        String stopReason,
        TokenUsage usage,
        Map<String, Object> metadata
) {

    public UnifiedChatResponse {
        if (provider == null) {
            throw new IllegalArgumentException("provider must not be null");
        }

        content = content == null ? "" : content;
        usage = usage == null ? TokenUsage.empty() : usage;
        metadata = metadata == null ? Map.of() : Map.copyOf(metadata);
    }
}
```
