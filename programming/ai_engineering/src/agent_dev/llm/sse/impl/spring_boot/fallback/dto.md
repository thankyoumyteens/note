# 统一 DTO

## 枚举

```java
package com.example.llm.dto;

public enum LlmProvider {
    OPENAI,
    ANTHROPIC,
    DEEPSEEK
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

## 统一请求：UnifiedChatRequest

```java
package com.example.llm.dto;

import java.util.List;
import java.util.Map;

/**
 * 统一聊天请求。
 * system 单独放，messages 只放用户和助手消息，方便同时适配 OpenAI 和 Anthropic。
 */
public record UnifiedChatRequest(
        String system, // 系统指令，用于设置模型的角色、行为规则和回答边界。
        List<UnifiedChatMessage> messages, // 对话消息列表。只放 user / assistant 消息，不放 system 消息。
        LlmGenerationOptions options, // 控制模型输出行为的参数。
        Map<String, Object> metadata // 扩展元数据。用于存放 provider、requestId、traceId、previousResponseId 等非标准字段。
) {

    public UnifiedChatRequest {
        messages = messages == null ? List.of() : List.copyOf(messages);
        metadata = metadata == null ? Map.of() : Map.copyOf(metadata);
        options = options == null ? LlmGenerationOptions.defaultOptions() : options;

        if (messages.isEmpty()) {
            throw new IllegalArgumentException("messages must not be empty");
        }
    }

    /**
     * 统一生成参数。
     * 不同 provider 参数名不同，但业务层统一使用这套字段。
     */
    public record LlmGenerationOptions(
            Double temperature, // 控制模型输出随机性，值越高输出越发散。
            Integer maxTokens, // 限制模型最多生成的 token 数。
            Double topP // nucleus sampling 参数，用于控制候选 token 的采样范围。
    ) {

        public static LlmGenerationOptions defaultOptions() {
            return new LlmGenerationOptions(
                    0.2,
                    1000,
                    null
            );
        }
    }
}
```

## Token 用量：TokenUsage

```java
package com.example.llm.dto;

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

## StreamEventType

```java
package com.example.llm.dto;

public enum StreamEventType {
    MESSAGE,
    DONE,
    ERROR,
    HEARTBEAT
}
```

## UnifiedChatStreamEvent

```java
package com.example.llm.dto;

import java.util.Map;

/**
 * 统一 stream 事件。
 * ProviderClient 输出这个对象，Controller 再转换为 SSE event。
 */
public record UnifiedChatStreamEvent(
        StreamEventType type, // 事件类型，例如 MESSAGE、DONE、ERROR、HEARTBEAT。
        LlmProvider provider, // 实际输出该事件的模型服务提供方。
        String model, // 实际使用的模型名称。
        String content, // MESSAGE 事件中的增量文本内容。
        String errorCode, // ERROR 事件中的错误码。
        String errorMessage, // ERROR 事件中的安全错误提示。
        TokenUsage usage, // DONE 事件中携带的 token 用量信息。
        Map<String, Object> metadata // 扩展元数据，用于存放 provider 特有字段、traceId、响应 id 等信息。
) {

    public UnifiedChatStreamEvent {
        content = content == null ? "" : content;
        errorCode = errorCode == null ? "" : errorCode;
        errorMessage = errorMessage == null ? "" : errorMessage;
        usage = usage == null ? TokenUsage.empty() : usage;
        metadata = metadata == null ? Map.of() : Map.copyOf(metadata);
    }

    public static UnifiedChatStreamEvent message(
            LlmProvider provider,
            String model,
            String content
    ) {
        return new UnifiedChatStreamEvent(
                StreamEventType.MESSAGE,
                provider,
                model,
                content,
                "",
                "",
                TokenUsage.empty(),
                Map.of()
        );
    }

    public static UnifiedChatStreamEvent done(
            LlmProvider provider,
            String model,
            TokenUsage usage
    ) {
        return new UnifiedChatStreamEvent(
                StreamEventType.DONE,
                provider,
                model,
                "",
                "",
                "",
                usage,
                Map.of()
        );
    }

    public static UnifiedChatStreamEvent error(
            String errorCode,
            String errorMessage
    ) {
        return new UnifiedChatStreamEvent(
                StreamEventType.ERROR,
                null,
                null,
                "",
                errorCode,
                errorMessage,
                TokenUsage.empty(),
                Map.of()
        );
    }

    public static UnifiedChatStreamEvent heartbeat() {
        return new UnifiedChatStreamEvent(
                StreamEventType.HEARTBEAT,
                null,
                null,
                "",
                "",
                "",
                TokenUsage.empty(),
                Map.of()
        );
    }

    public static UnifiedChatStreamEvent message(
            LlmProvider provider,
            String model,
            String content,
            Map<String, Object> metadata
    ) {
        return new UnifiedChatStreamEvent(
                StreamEventType.MESSAGE,
                provider,
                model,
                content,
                "",
                "",
                TokenUsage.empty(),
                metadata
        );
    }

    public static UnifiedChatStreamEvent done(
            LlmProvider provider,
            String model,
            TokenUsage usage,
            Map<String, Object> metadata
    ) {
        return new UnifiedChatStreamEvent(
                StreamEventType.DONE,
                provider,
                model,
                "",
                "",
                "",
                usage,
                metadata
        );
    }
}
```
