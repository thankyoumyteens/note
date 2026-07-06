# 统一 DTO

## LlmProvider

```java id="pry2n9"
package com.example.llm.dto;

public enum LlmProvider {
    OPENAI,
    ANTHROPIC,
    DEEPSEEK
}
```

## ChatRole

```java id="zknivw"
package com.example.llm.dto;

public enum ChatRole {
    USER,
    ASSISTANT
}
```

## UnifiedChatMessage

```java id="c3fnxu"
package com.example.llm.dto;

/**
 * 统一消息结构。
 * 为了兼容 OpenAI 和 Anthropic，只保留 USER / ASSISTANT。
 */
public record UnifiedChatMessage(
        ChatRole role, // 消息角色。
        String content // 消息内容。
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

## UnifiedChatRequest

```java id="gu7f14"
package com.example.llm.dto;

import java.util.List;
import java.util.Map;

/**
 * 统一聊天请求。
 * system 单独放，messages 只放用户和助手消息，方便同时适配 OpenAI 和 Anthropic。
 */
public record UnifiedChatRequest(
        String system, // 系统指令，用于设置模型的角色、行为规则和回答边界。
        List<UnifiedChatMessage> messages, // 对话消息列表，只放 user / assistant。
        LlmGenerationOptions options, // 控制模型输出行为的参数。
        Map<String, Object> metadata // 扩展元数据，例如 requestId、traceId、用户信息等。
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
     */
    public record LlmGenerationOptions(
            Double temperature, // 控制模型输出随机性。
            Integer maxTokens, // 限制模型最多生成多少 token。
            Double topP // nucleus sampling 参数。
    ) {

        public static LlmGenerationOptions defaultOptions() {
            return new LlmGenerationOptions(0.2, 1000, null);
        }
    }
}
```

## TokenUsage

```java id="yvv8cs"
package com.example.llm.dto;

/**
 * 统一 token usage。
 */
public record TokenUsage(
        Integer inputTokens, // 输入 token 数。
        Integer outputTokens, // 输出 token 数。
        Integer totalTokens // token 总数。
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

```java id="jssyvb"
package com.example.llm.dto;

public enum StreamEventType {
    MESSAGE,
    DONE,
    ERROR,
    HEARTBEAT
}
```

## UnifiedChatStreamEvent

```java id="89nnlj"
package com.example.llm.dto;

import java.util.Map;

/**
 * 统一 stream 事件。
 * ProviderClient 输出这个对象，Controller 再转换为 SSE event。
 */
public record UnifiedChatStreamEvent(
        StreamEventType type, // 事件类型。
        LlmProvider provider, // 实际输出该事件的 provider。
        String model, // 实际使用的模型名称。
        String content, // message 事件中的增量文本。
        String errorCode, // error 事件中的错误码。
        String errorMessage, // error 事件中的安全错误提示。
        TokenUsage usage, // done 事件中的 token usage。
        Map<String, Object> metadata // 附加元数据，例如 Spring AI metadata、requestId、provider 信息等。
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
}
```

## StreamEventResponse

```java id="d8q4lz"
package com.example.llm.dto;

/**
 * 返回给前端的 SSE JSON 数据。
 */
public record StreamEventResponse(
        String content, // message 事件中的增量文本内容。
        String code, // error 事件中的错误码。
        String message, // error 事件中的安全错误提示。
        Boolean done // 是否表示流式响应已经结束。
) {

    public static StreamEventResponse messageEvent(String content) {
        return new StreamEventResponse(content, "", "", false);
    }

    public static StreamEventResponse error(String code, String message) {
        return new StreamEventResponse("", code, message, false);
    }

    public static StreamEventResponse doneEvent() {
        return new StreamEventResponse("", "", "", true);
    }

    public static StreamEventResponse heartbeat() {
        return new StreamEventResponse("", "", "", false);
    }
}
```
