# 统一消息对象

```java
package com.example.llm.dto;

/**
 * 统一的 LLM 消息对象，用于表示一条对话消息。
 * role 表示消息角色，content 表示消息内容。
 */
public record LlmMessage(
        String role,
        String content
) {

    /**
     * 创建 system 消息，用于设置模型行为和回答规则。
     */
    public static LlmMessage system(String content) {
        return new LlmMessage("system", content);
    }

    /**
     * 创建 user 消息，用于表示用户输入。
     */
    public static LlmMessage user(String content) {
        return new LlmMessage("user", content);
    }

    /**
     * 创建 assistant 消息，用于表示模型历史回复。
     */
    public static LlmMessage assistant(String content) {
        return new LlmMessage("assistant", content);
    }
}
```
