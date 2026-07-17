# RenderedPrompt

```java
package com.example.llm.prompt;

/**
 * 一次模板渲染后的最终 Prompt。
 */
public record RenderedPrompt(
        String promptName, // 本次使用的 Prompt 名称。
        String promptVersion, // 本次使用的 Prompt 版本。
        String system, // 渲染后的 system 消息。
        String user // 渲染后的 user 消息。
) {

    public RenderedPrompt {
        if (promptName == null || promptName.isBlank()) {
            throw new IllegalArgumentException("promptName must not be blank");
        }

        if (promptVersion == null || promptVersion.isBlank()) {
            throw new IllegalArgumentException("promptVersion must not be blank");
        }

        if (system == null || system.isBlank()) {
            throw new IllegalArgumentException("system must not be blank");
        }

        if (user == null || user.isBlank()) {
            throw new IllegalArgumentException("user must not be blank");
        }
    }
}
```

`RenderedPrompt` 保留名称和版本，后续可以写入统一请求的 metadata，便于定位一次调用使用了哪个模板。
