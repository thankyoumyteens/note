# 改造 TaskExtractionService

把你的 `TaskExtractionService` 改成下面这个版本。

重点新增：

```text
1. 最多尝试 2 次
2. 第一次正常抽取
3. 失败后调用 repairJson
4. 对结果做字段校验
5. 对 priority 做容错
6. 把原始输出和修复输出打印出来
```

````java
package com.example.aigateway.service;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.dto.TaskExtractionResult;
import com.example.aigateway.dto.TaskPriority;
import com.example.aigateway.exception.AiStructuredOutputException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

@Service
public class TaskExtractionService {

    private final LlmClient llmClient;
    private final ObjectMapper objectMapper;

    public TaskExtractionService(LlmClient llmClient, ObjectMapper objectMapper) {
        this.llmClient = llmClient;
        this.objectMapper = objectMapper;
    }

    public TaskExtractionResult extract(String text) {
        if (text == null || text.isBlank()) {
            throw new IllegalArgumentException("text cannot be empty");
        }

        String raw = llmClient.complete(buildExtractionSystemPrompt(), text);
        System.out.println("LLM raw extraction output: " + raw);

        try {
            return parseAndValidate(raw);
        } catch (Exception firstError) {
            System.err.println("First parse failed: " + firstError.getMessage());

            String repaired = repairJson(raw, firstError.getMessage());
            System.out.println("LLM repaired extraction output: " + repaired);

            try {
                return parseAndValidate(repaired);
            } catch (Exception secondError) {
                throw new AiStructuredOutputException(
                        "Failed to parse structured task extraction output after repair",
                        raw,
                        secondError
                );
            }
        }
    }

    private TaskExtractionResult parseAndValidate(String raw) throws Exception {
        String json = cleanupJson(raw);
        TaskExtractionResult result = objectMapper.readValue(json, TaskExtractionResult.class);
        return normalizeAndValidate(result);
    }

    private String repairJson(String rawOutput, String errorMessage) {
        String systemPrompt = """
                你是一个 JSON 修复器。

                你的任务是把输入内容修复成合法 JSON。

                目标 JSON Schema：
                {
                  "taskName": "string",
                  "dueTimeText": "string or null",
                  "priority": "LOW | MEDIUM | HIGH | UNKNOWN",
                  "assignee": "string"
                }

                修复规则：
                - 只能输出合法 JSON
                - 不要输出 Markdown
                - 不要输出解释
                - 不要使用 ```json 代码块
                - 不要添加额外字段
                - 不要省略字段
                - 如果 dueTimeText 不存在，使用 null
                - 如果 assignee 不存在，使用 "me"
                - 如果 priority 不是 LOW、MEDIUM、HIGH、UNKNOWN 之一，请修复为最接近的枚举值
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

    private String buildExtractionSystemPrompt() {
        return """
                你是一个任务信息抽取器。

                你的任务是从用户输入中抽取待办事项信息。

                你只能输出 JSON，不能输出 Markdown，不能输出解释，不能使用 ```json 代码块。

                JSON 字段要求：
                {
                  "taskName": "待办事项名称，字符串",
                  "dueTimeText": "原文中的时间表达，如果没有则为 null",
                  "priority": "LOW | MEDIUM | HIGH | UNKNOWN",
                  "assignee": "负责人。如果用户没有指定，则为 me"
                }

                优先级判断规则：
                - 出现“紧急”、“尽快”、“马上”、“高优先级”、“优先级高”，priority = HIGH
                - 出现“一般”、“普通”，priority = MEDIUM
                - 出现“不急”、“有空”、“低优先级”，priority = LOW
                - 无法判断，priority = UNKNOWN

                注意：
                - 必须输出合法 JSON
                - 不要额外添加字段
                - 不要省略字段
                """;
    }

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

    private TaskExtractionResult normalizeAndValidate(TaskExtractionResult result) {
        if (result == null) {
            throw new IllegalStateException("result is null");
        }

        String taskName = blankToNull(result.taskName());
        String dueTimeText = blankToNull(result.dueTimeText());
        TaskPriority priority = result.priority() == null ? TaskPriority.UNKNOWN : result.priority();
        String assignee = blankToNull(result.assignee());

        if (taskName == null) {
            throw new IllegalStateException("taskName is required");
        }

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

    private String blankToNull(String value) {
        return value == null || value.isBlank() ? null : value.strip();
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
