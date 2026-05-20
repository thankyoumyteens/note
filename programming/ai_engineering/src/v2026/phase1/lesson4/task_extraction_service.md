# 新增 TaskExtractionService

文件：

```text
src/main/java/com/example/aigateway/service/TaskExtractionService.java
```

代码：

````java
package com.example.aigateway.service;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.dto.TaskExtractionResult;
import com.example.aigateway.dto.TaskPriority;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;

/**
 * 任务信息抽取服务。
 *
 * 负责：
 * 1. 构造结构化输出 Prompt
 * 2. 调用大模型
 * 3. 清理模型返回的 JSON
 * 4. 解析为 Java DTO
 * 5. 做基础字段规范化
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
                buildSystemPrompt(),
                text
        );

        String json = cleanupJson(rawOutput);

        try {
            TaskExtractionResult result = objectMapper.readValue(
                    json,
                    TaskExtractionResult.class
            );

            return normalize(result);

        } catch (Exception e) {
            throw new RuntimeException(
                    "Failed to parse task extraction result. rawOutput=" + rawOutput,
                    e
            );
        }
    }

    /**
     * 构造系统 Prompt。
     *
     * 这里明确要求模型只输出 JSON。
     * 但注意：Prompt 不是强约束，所以仍然需要后端清理和解析。
     */
    private String buildSystemPrompt() {
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
     * 清理模型输出中的 JSON。
     *
     * 第 4 课只做基础清理：
     * - 去掉 ```json
     * - 去掉 ```
     *
     * 第 5 课会增强为从任意文本中提取 { ... }。
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

        return text;
    }

    /**
     * 对模型解析后的结果做基础规范化。
     *
     * 本课只做基础处理：
     * - 字符串 trim
     * - priority 为空时转 UNKNOWN
     * - assignee 为空时转 me
     * - taskName 为空时报错
     */
    private TaskExtractionResult normalize(TaskExtractionResult result) {
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
     * 空字符串会转成 null。
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
