# 新增 TaskExtractionService

新建：

```text
service/TaskExtractionService.java
```

代码：

````java
package com.example.aigateway.service;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.dto.TaskExtractionResult;
import com.example.aigateway.dto.TaskPriority;
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

        String systemPrompt = """
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

        String raw = llmClient.complete(systemPrompt, text);
        // 观察模型到底返回了什么
        System.out.println("LLM raw extraction output: " + raw);

        String json = cleanupJson(raw);

        try {
            TaskExtractionResult result = objectMapper.readValue(json, TaskExtractionResult.class);
            return normalize(result);
        } catch (Exception e) {
            throw new RuntimeException("Failed to parse task extraction result. raw=" + raw, e);
        }
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

        return text;
    }

    private TaskExtractionResult normalize(TaskExtractionResult result) {
        String taskName = blankToNull(result.taskName());
        String dueTimeText = blankToNull(result.dueTimeText());
        TaskPriority priority = result.priority() == null ? TaskPriority.UNKNOWN : result.priority();
        String assignee = blankToNull(result.assignee());

        if (assignee == null) {
            assignee = "me";
        }

        if (taskName == null) {
            throw new IllegalStateException("taskName is required");
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
