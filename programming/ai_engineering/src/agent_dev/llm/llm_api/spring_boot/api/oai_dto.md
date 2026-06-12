# OpenAI-compatible 请求和响应对象

OpenAI / Qwen / DeepSeek 都可以先走这个对象。

## 请求对象

把 Java 对象映射成 OpenAI-compatible Chat Completions API 的请求 JSON。

```java
package com.example.llm.dto.openai;

import com.example.llm.dto.LlmMessage;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * OpenAI-compatible Chat Completions API 的请求体 DTO。
 * 适用于 OpenAI 风格的 /chat/completions 接口
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record OpenAiChatRequest(

        /**
         * 要调用的模型名称。
         */
        String model,

        /**
         * 对话消息列表。
         * 用来告诉模型当前对话的上下文。
         */
        List<LlmMessage> messages,

        /**
         * 控制模型输出随机性的参数。
         * temperature 越低，模型输出越稳定、越保守；
         * temperature 越高，模型输出越发散、越有创造性。
         */
        Double temperature,

        /**
         * 限制模型最多生成多少 token。
         * 注意：
         * 这个参数只限制输出长度，不限制输入长度。
         * 输入 messages 的长度仍然受模型上下文窗口限制。
         */
        @JsonProperty("max_tokens")
        Integer maxTokens,

        /**
         * 是否启用流式输出。
         */
        Boolean stream
) {
}
```

## 响应对象

```java
package com.example.llm.dto.openai;

import java.util.List;

/**
 * OpenAI-compatible Chat Completions API 的响应体。
 * 这里只保留 choices.message.content，方便获取模型回答文本。
 */
public record OpenAiChatResponse(
        List<Choice> choices
) {

    /**
     * 获取第一个候选回答的文本内容。
     * 如果响应为空或没有 content，则返回空字符串，避免空指针异常。
     */
    public String firstText() {
        if (choices == null || choices.isEmpty()) {
            return "";
        }

        // 普通聊天场景通常只取第一个候选结果。
        Message message = choices.getFirst().message();

        // message 或 content 为空时返回空字符串，保证调用方拿到稳定的 String。
        return message == null || message.content() == null ? "" : message.content();
    }

    /**
     * 单个候选结果。
     * 当前只关心其中的 message 字段。
     */
    public record Choice(
            Message message
    ) {
    }

    /**
     * 模型返回的消息内容。
     * role 通常是 assistant，content 是最终回答文本。
     */
    public record Message(
            String role,
            String content
    ) {
    }
}
```
