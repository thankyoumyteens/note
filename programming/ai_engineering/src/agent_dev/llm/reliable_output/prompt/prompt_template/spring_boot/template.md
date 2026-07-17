# PromptTemplate

```java
package com.example.llm.prompt;

/**
 * Prompt 模板定义，只保存稳定规则和变量占位符。
 */
public record PromptTemplate(
        String name, // Prompt 名称，例如 intent-classifier。
        String version, // Prompt 版本，例如 v1。
        String systemTemplate, // system prompt 模板。
        String userTemplate // user prompt 模板。
) {

    public PromptTemplate {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("name must not be blank");
        }

        if (version == null || version.isBlank()) {
            throw new IllegalArgumentException("version must not be blank");
        }

        if (systemTemplate == null || systemTemplate.isBlank()) {
            throw new IllegalArgumentException("systemTemplate must not be blank");
        }

        if (userTemplate == null || userTemplate.isBlank()) {
            throw new IllegalArgumentException("userTemplate must not be blank");
        }
    }
}
```

模板使用 `{{变量名}}` 表示动态值。名称和版本在创建时确定，业务调用只能传入变量，不能临时修改固定规则。
