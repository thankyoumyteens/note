# 统一 DTO

## 枚举

```java
public enum LlmProvider {
    OPENAI,
    ANTHROPIC,
    DEEPSEEK
}
```

```java
public enum ChatRole {
    USER,
    ASSISTANT
}
```

## 统一消息：UnifiedChatMessage

```java
/**
 * 统一消息结构。
 * 为了兼容 OpenAI 和 Anthropic，基础聊天阶段只保留 USER / ASSISTANT。
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
/**
 * 统一生成参数。
 * 不同 provider 参数名不同，但业务层统一使用这套字段。
 */
public record LlmGenerationOptions(
        Double temperature,
        Integer maxTokens,
        Double topP
) {

    public static LlmGenerationOptions defaultOptions() {
        return new LlmGenerationOptions(
                0.2,
                1000,
                null
        );
    }
}
```

## 统一请求：UnifiedChatRequest

```java
import java.util.List;
import java.util.Map;

/**
 * 统一聊天请求。
 * system 单独放，messages 只放用户和助手消息，方便同时适配 OpenAI 和 Anthropic。
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

    public static UnifiedChatRequest user(String message) {
        return new UnifiedChatRequest(
                null,
                List.of(UnifiedChatMessage.user(message)),
                LlmGenerationOptions.defaultOptions(),
                Map.of()
        );
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
/**
 * 统一 token usage。
 * OpenAI 和 Anthropic 都能映射到 input / output / total。
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
import java.util.Map;

/**
 * 统一聊天响应。
 * provider 表示最终实际命中的模型服务，不一定是第一候选 provider。
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

        if (content == null) {
            content = "";
        }

        metadata = metadata == null ? Map.of() : Map.copyOf(metadata);
    }
}
```
