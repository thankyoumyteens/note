# VersionedPromptTemplate

Spring AI 的 `PromptTemplate` 负责变量渲染；`VersionedPromptTemplate` 只补充业务模板的名称和版本。

```java
package com.example.llm.prompt;

import org.springframework.ai.chat.prompt.PromptTemplate;

import java.util.Map;

/**
 * 带名称和版本的 Spring AI Prompt 模板。
 */
public record VersionedPromptTemplate(
        String name, // Prompt 名称，例如 intent-classifier。
        String version, // Prompt 版本，例如 v1。
        PromptTemplate systemTemplate, // Spring AI system 模板。
        PromptTemplate userTemplate // Spring AI user 模板。
) {

    public VersionedPromptTemplate {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("name must not be blank");
        }

        if (version == null || version.isBlank()) {
            throw new IllegalArgumentException("version must not be blank");
        }

        if (systemTemplate == null) {
            throw new IllegalArgumentException("systemTemplate must not be null");
        }

        if (userTemplate == null) {
            throw new IllegalArgumentException("userTemplate must not be null");
        }
    }

    public RenderedPrompt render(Map<String, Object> variables) {
        Map<String, Object> safeVariables = variables == null
                ? Map.of()
                : Map.copyOf(variables);

        return new RenderedPrompt(
                name,
                version,
                systemTemplate.render(),
                userTemplate.render(safeVariables)
        );
    }

    /**
     * 一次渲染后的最终 system、user 消息。
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
}
```

Spring AI 默认使用 `{变量名}` 占位符。变量缺失或模板无法渲染时，由 Spring AI 的模板渲染器抛出异常。
