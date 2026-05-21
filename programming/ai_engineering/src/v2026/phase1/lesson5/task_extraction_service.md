# 改造 TaskExtractionService

文件：

```text
src/main/java/com/example/aigateway/service/TaskExtractionService.java
```

用下面版本替换你当前的 `TaskExtractionService`：

````java
package com.example.aigateway.service;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.dto.TaskExtractionResult;
import com.example.aigateway.dto.TaskPriority;
import com.example.aigateway.exception.AiStructuredOutputException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

/**
 * 任务信息抽取服务。
 *
 * 第 5 课增强点：
 * 1. 从模型输出中提取 { ... }
 * 2. 统一 parseAndValidate
 * 3. JSON 解析失败后自动 repair 一次
 * 4. 修复后再次解析
 * 5. 仍失败则抛出 AiStructuredOutputException
 */
@Service
public class TaskExtractionService {

    private final LlmClient llmClient;
    private final ObjectMapper objectMapper;

    public TaskExtractionService(
            LlmClient llmClient,
            ObjectMapper objectMapper
    ) {
        this.llmClient = llmClient;
        this.objectMapper = objectMapper;
    }

    /**
     * 从自然语言文本中抽取任务信息。
     */
    public TaskExtractionResult extract(String text) {
        if (text == null || text.isBlank()) {
            throw new IllegalArgumentException("text cannot be empty");
        }

        String rawOutput = llmClient.complete(
                buildExtractionSystemPrompt(),
                text
        );

        System.out.println("LLM raw extraction output: " + rawOutput);

        try {
            return parseAndValidate(rawOutput);
        } catch (Exception firstError) {
            System.err.println("First parse failed: " + firstError.getMessage());

            String repairedOutput = repairJson(rawOutput, firstError.getMessage());

            System.out.println("LLM repaired extraction output: " + repairedOutput);

            try {
                return parseAndValidate(repairedOutput);
            } catch (Exception secondError) {
                throw new AiStructuredOutputException(
                        "Failed to parse structured task extraction output after repair",
                        rawOutput,
                        secondError
                );
            }
        }
    }

    /**
     * 解析并校验模型输出。
     *
     * 这个方法会被调用两次：
     * 1. 第一次解析原始模型输出
     * 2. 第二次解析修复后的模型输出
     */
    private TaskExtractionResult parseAndValidate(String raw) throws Exception {
        String json = cleanupJson(raw);

        TaskExtractionResult result = objectMapper.readValue(
                json,
                TaskExtractionResult.class
        );

        return normalizeAndValidate(result);
    }

    /**
     * 构造任务抽取 system prompt。
     */
    private String buildExtractionSystemPrompt() {
        return """
                你是一个任务信息抽取器。
                
                你的任务是从用户输入中抽取待办任务信息。
                
                你只能输出 JSON，不能输出 Markdown，不能输出解释，不能使用 ```json 代码块。
                
                JSON 字段要求：
                {
                  "taskName": "待办事项名称，字符串，不能为空",
                  "dueTimeText": "原文中的时间表达，如果没有则为 null",
                  "priority": "LOW | MEDIUM | HIGH | UNKNOWN",
                  "assignee": "负责人。如果用户没有指定，则为 me"
                }
                
                字段规则：
                - taskName 应该是简短动作短语，不要包含“用户想”“提醒我”等多余描述
                - dueTimeText 保留用户原文中的时间表达，不要自行换算成日期
                - priority 只能是 LOW、MEDIUM、HIGH、UNKNOWN
                - 如果用户说“高优先级”“紧急”“很急”，priority = HIGH
                - 如果用户说“不急”“有空再做”，priority = LOW
                - 如果无法判断优先级，priority = UNKNOWN
                - 如果没有指定负责人，assignee = "me"
                """;
    }

    /**
     * JSON 修复。
     *
     * 注意：
     * 这里不是重新抽取任务，而是让模型把错误输出修复成合法 JSON。
     */
    private String repairJson(String rawOutput, String errorMessage) {
        String systemPrompt = """
                你是一个 JSON 修复器。
                
                你的任务是把错误的模型输出修复为合法 JSON。
                
                你只能输出 JSON，不能输出 Markdown，不能输出解释，不能使用 ```json 代码块。
                
                目标 JSON 格式：
                {
                  "taskName": "待办事项名称，字符串，不能为空",
                  "dueTimeText": "原文中的时间表达，如果没有则为 null",
                  "priority": "LOW | MEDIUM | HIGH | UNKNOWN",
                  "assignee": "负责人。如果用户没有指定，则为 me"
                }
                
                修复规则：
                - 不要添加目标格式以外的字段
                - 不要省略目标格式中的字段
                - priority 必须是 LOW、MEDIUM、HIGH、UNKNOWN 之一
                - 如果 priority 是中文，例如“高”“紧急”，请映射为 HIGH
                - 如果 priority 是“不急”，请映射为 LOW
                - 如果无法判断 priority，请使用 UNKNOWN
                - 如果 assignee 缺失或为空，请使用 "me"
                - 如果 dueTimeText 缺失或为空，请使用 null
                """;

        String userPrompt = """
                原始模型输出：
                %s
                
                解析错误：
                %s
                
                请修复为合法 JSON。
                """.formatted(rawOutput, errorMessage);

        return llmClient.complete(systemPrompt, userPrompt);
    }

    /**
     * 清理模型输出中的 JSON。
     *
     * 第 5 课增强点：
     * - 去掉 Markdown 代码块
     * - 从文本中截取第一个 { 到最后一个 }
     *
     * 这样可以处理：
     * “以下是结果：{...}”
     */
    private String cleanupJson(String raw) {
        if (raw == null) {
            throw new IllegalStateException("LLM output is null");
        }

        String text = raw.strip();

        if (text.startsWith("```json")) {
            text = text.substring("```json".length()).strip();
        }

        if (text.startsWith("```")) {
            text = text.substring("```".length()).strip();
        }

        if (text.endsWith("```")) {
            text = text.substring(0, text.length() - 3).strip();
        }

        int firstBrace = text.indexOf('{');
        int lastBrace = text.lastIndexOf('}');

        if (firstBrace >= 0 && lastBrace > firstBrace) {
            text = text.substring(firstBrace, lastBrace + 1).strip();
        }

        return text;
    }

    /**
     * 规范化并校验结构化输出结果。
     */
    private TaskExtractionResult normalizeAndValidate(TaskExtractionResult result) {
        if (result == null) {
            throw new IllegalStateException("Task extraction result is null");
        }

        String taskName = normalizeRequiredString(
                result.taskName(),
                "taskName cannot be empty"
        );

        String dueTimeText = normalizeNullableString(result.dueTimeText());

        TaskPriority priority = result.priority() == null
                ? TaskPriority.UNKNOWN
                : result.priority();

        String assignee = normalizeNullableString(result.assignee());
        if (assignee == null) {
            assignee = "me";
        }

        return new TaskExtractionResult(
                taskName,
                dueTimeText,
                priority,
                assignee
        );
    }

    /**
     * 规范化必填字符串。
     */
    private String normalizeRequiredString(String value, String errorMessage) {
        String normalized = normalizeNullableString(value);

        if (normalized == null) {
            throw new IllegalArgumentException(errorMessage);
        }

        return normalized;
    }

    /**
     * 规范化可空字符串。
     *
     * null -> null
     * "" -> null
     * "  abc  " -> "abc"
     */
    private String normalizeNullableString(String value) {
        if (value == null) {
            return null;
        }

        String normalized = value.strip();

        return normalized.isEmpty() ? null : normalized;
    }
}
````

## 为什么需要自动修复？

即使做了 JSON 清理，仍然可能遇到模型输出不合法的情况。

例如：

```json
{
  "taskName": "给张三发报价单",
  "dueTimeText": "明天下午三点",
  "priority": "高",
  "assignee": "me"
}
```

这里 JSON 格式可能合法，但 `priority` 不符合 Java enum。

或者：

```json
{
  "taskName": "给张三发报价单",
  "dueTimeText": "明天下午三点"
}
```

这里字段名没有引号，不是合法 JSON。

这种情况可以把：

```text
原始模型输出
解析错误信息
目标 JSON Schema
```

再次发给模型，让模型修复成合法 JSON。

这就是 `repairJson()`。

## 为什么不能无限修复？

自动修复虽然有用，但不能无限重试。

原因：

- 每次修复都是一次模型调用，会增加成本
- 会增加接口耗时
- 如果模型持续失败，重试也可能无效
- 无限重试可能导致请求卡住
- 不利于排查真实问题

当前策略：

```text
最多修复一次。
```

也就是：

```text
第一次解析失败 -> 修复一次 -> 再失败就抛异常
```

这是一个合理的入门生产策略。
