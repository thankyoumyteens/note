# PromptRegistry

PromptDefinition.java

```java
package com.example.llm.prompt;

import com.example.llm.dto.ChatRole;
import com.example.llm.dto.UnifiedChatMessage;

import java.util.List;

/**
 * 一个不可变的完整 Spring AI Prompt 版本。
 */
public record PromptDefinition(
        VersionedPromptTemplate template, // 带名称和版本的 Spring AI 模板。
        List<UnifiedChatMessage> examples // 该版本固定的 Few-shot 消息。
) {

    public PromptDefinition {
        if (template == null) {
            throw new IllegalArgumentException("template must not be null");
        }

        examples = examples == null ? List.of() : List.copyOf(examples);
        validateExamples(examples);
    }

    private static void validateExamples(List<UnifiedChatMessage> examples) {
        if (examples.size() % 2 != 0) {
            throw new IllegalArgumentException("Few-shot messages must contain complete pairs");
        }

        for (int index = 0; index < examples.size(); index += 2) {
            if (examples.get(index).role() != ChatRole.USER
                    || examples.get(index + 1).role() != ChatRole.ASSISTANT) {
                throw new IllegalArgumentException("Few-shot messages must alternate USER and ASSISTANT");
            }
        }
    }
}
```

PromptSelection.java

```java
package com.example.llm.prompt;

/**
 * 应用当前启用的 Prompt 名称和版本。
 */
public record PromptSelection(
        String name, // Prompt 稳定名称。
        String version // 当前启用版本。
) {

    public PromptSelection {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("name must not be blank");
        }
        if (version == null || version.isBlank()) {
            throw new IllegalArgumentException("version must not be blank");
        }
    }
}
```

PromptRegistry.java

```java
package com.example.llm.prompt;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 按名称和版本精确查找 Prompt 定义的只读注册表。
 */
public final class PromptRegistry {

    // 应用启动时构造，运行期间不修改的版本索引。
    private final Map<PromptKey, PromptDefinition> definitions;

    public PromptRegistry(List<PromptDefinition> definitions) {
        if (definitions == null || definitions.isEmpty()) {
            throw new IllegalArgumentException("definitions must not be empty");
        }

        Map<PromptKey, PromptDefinition> index = new HashMap<>();
        for (PromptDefinition definition : List.copyOf(definitions)) {
            if (definition == null) {
                throw new IllegalArgumentException("definition must not be null");
            }

            PromptKey key = new PromptKey(
                    definition.template().name(),
                    definition.template().version()
            );
            if (index.putIfAbsent(key, definition) != null) {
                throw new IllegalArgumentException("Duplicate prompt version: " + key);
            }
        }
        this.definitions = Map.copyOf(index);
    }

    public PromptDefinition require(PromptSelection selection) {
        if (selection == null) {
            throw new IllegalArgumentException("selection must not be null");
        }

        PromptKey key = new PromptKey(selection.name(), selection.version());
        PromptDefinition definition = definitions.get(key);
        if (definition == null) {
            throw new IllegalArgumentException("Prompt version not found: " + key);
        }
        return definition;
    }

    private record PromptKey(
            String name, // Prompt 稳定名称。
            String version // Prompt 版本。
    ) {}
}
```

Registry 的职责只包含启动校验和精确查找；它不根据版本字符串推断“最新版本”。
