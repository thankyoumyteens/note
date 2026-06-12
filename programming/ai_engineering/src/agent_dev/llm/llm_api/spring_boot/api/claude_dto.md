# Claude 请求和响应对象

Claude 原生 Messages API 的格式和 OpenAI 不一样。

## 请求对象

```java
package com.example.llm.dto.claude;

import com.example.llm.dto.LlmMessage;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * Claude Messages API 的请求体 DTO。
 * Claude 的 system 是单独字段，不放在 messages 列表里。
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record ClaudeMessageRequest(
        /**
         * 要调用的 Claude 模型名称。
         */
        String model,

        /**
         * 限制模型最多生成多少 token。
         * Java 使用 maxTokens，JSON 中需要序列化为 max_tokens。
         */
        @JsonProperty("max_tokens")
        Integer maxTokens,

        /**
         * 系统指令，用于设置模型的角色、行为和回答规则。
         */
        String system,

        /**
         * 对话消息列表，只包含 user / assistant 消息。
         * Claude 原生 API 不把 system 放进 messages。
         */
        List<LlmMessage> messages
) {
}
```

## 响应对象

```java
package com.example.llm.dto.claude;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Claude Messages API 的响应体 DTO。
 * 这里只提取 content 中的文本块，方便获取模型回答。
 */
public record ClaudeMessageResponse(
        List<ContentBlock> content
) {

    /**
     * 拼接 Claude 返回的所有 text 内容块。
     * 如果响应为空，则返回空字符串，避免空指针异常。
     */
    public String text() {
        if (content == null || content.isEmpty()) {
            return "";
        }

        return content.stream()
                // Claude 的 content 里可能有多种 block，这里只保留文本类型。
                .filter(block -> "text".equals(block.type()))

                // 取出每个文本块中的 text 字段。
                .map(ContentBlock::text)

                // 过滤空文本，避免返回多余空行。
                .filter(text -> text != null && !text.isBlank())

                // 如果有多个文本块，用换行拼接成完整回答。
                .collect(Collectors.joining("\n"));
    }

    /**
     * Claude 响应中的单个内容块。
     * type 表示内容类型，text 表示文本内容。
     */
    public record ContentBlock(
            String type,
            String text
    ) {
    }
}
```
