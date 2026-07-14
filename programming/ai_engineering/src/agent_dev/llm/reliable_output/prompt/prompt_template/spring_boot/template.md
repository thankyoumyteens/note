# PromptTemplate

```java
package com.example.llm.prompt;

/**
 * Prompt 模板定义。
 * name/version 用于版本管理，systemTemplate/userTemplate 用于生成最终 prompt。
 */
public record PromptTemplate(
        String name, // Prompt 名称，例如 intent-classifier。
        String version, // Prompt 版本，例如 v1。
        String systemTemplate, // system prompt 模板。
        String userTemplate // user prompt 模板。
) {
}
```
