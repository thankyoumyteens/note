# PromptRenderer

```java
package com.example.llm.prompt;

import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * 校验模板变量并生成最终 system、user 消息。
 */
public final class PromptRenderer {

    // 匹配 {{variable_name}} 形式的占位符。
    private static final Pattern PLACEHOLDER = Pattern.compile("\\{\\{([a-zA-Z][a-zA-Z0-9_]*)}}");

    public RenderedPrompt render(PromptTemplate template, Map<String, String> variables) {
        if (template == null) {
            throw new IllegalArgumentException("template must not be null");
        }

        Map<String, String> safeVariables = variables == null ? Map.of() : Map.copyOf(variables);
        Set<String> requiredVariables = placeholdersOf(template);

        validateVariables(requiredVariables, safeVariables);

        return new RenderedPrompt(
                template.name(),
                template.version(),
                replace(template.systemTemplate(), safeVariables),
                replace(template.userTemplate(), safeVariables)
        );
    }

    private Set<String> placeholdersOf(PromptTemplate template) {
        Set<String> placeholders = new HashSet<>();
        placeholders.addAll(placeholdersOf(template.systemTemplate()));
        placeholders.addAll(placeholdersOf(template.userTemplate()));
        return Set.copyOf(placeholders);
    }

    private Set<String> placeholdersOf(String content) {
        Set<String> placeholders = new HashSet<>();
        Matcher matcher = PLACEHOLDER.matcher(content);

        while (matcher.find()) {
            placeholders.add(matcher.group(1));
        }

        return placeholders;
    }

    private void validateVariables(Set<String> required, Map<String, String> actual) {
        Set<String> missing = new HashSet<>(required);
        missing.removeAll(actual.keySet());

        if (!missing.isEmpty()) {
            throw new IllegalArgumentException("Missing prompt variables: " + missing);
        }

        Set<String> unused = new HashSet<>(actual.keySet());
        unused.removeAll(required);

        if (!unused.isEmpty()) {
            throw new IllegalArgumentException("Unused prompt variables: " + unused);
        }

        required.forEach(name -> {
            String value = actual.get(name);

            if (value == null || value.isBlank()) {
                throw new IllegalArgumentException("Prompt variable must not be blank: " + name);
            }
        });
    }

    private String replace(String content, Map<String, String> variables) {
        Matcher matcher = PLACEHOLDER.matcher(content);
        StringBuilder result = new StringBuilder();

        while (matcher.find()) {
            String value = variables.get(matcher.group(1));
            // quoteReplacement 防止变量中的 $ 和反斜杠被正则替换规则解释。
            matcher.appendReplacement(result, Matcher.quoteReplacement(value));
        }

        matcher.appendTail(result);
        return result.toString();
    }
}
```

这里把全部占位符都视为必填变量，同时拒绝未使用变量，避免变量名拼错后静默发送错误 Prompt。正则转义只保证模板可以正确渲染，不代表能够消除 Prompt Injection；固定规则仍需放在 system 模板，用户输入只放在明确的数据边界内。
