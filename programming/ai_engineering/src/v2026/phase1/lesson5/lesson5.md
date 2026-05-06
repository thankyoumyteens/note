# 第 5 课：结构化输出稳定性增强

## 本课目标

把现在的流程：

```text
模型输出 JSON -> Jackson 解析 -> 成功或报错
```

升级为：

```text
模型输出 JSON
  -> 清理 JSON
  -> Jackson 解析
  -> 字段校验
  -> 如果失败，自动让模型修复 JSON
  -> 再次解析
  -> 仍失败才返回明确错误
```

---

## 当前问题

现在的 `TaskExtractionService` 大概是：

```java
String raw = llmClient.complete(systemPrompt, text);
String json = cleanupJson(raw);

try {
    TaskExtractionResult result = objectMapper.readValue(json, TaskExtractionResult.class);
    return normalize(result);
} catch (Exception e) {
    throw new RuntimeException("Failed to parse task extraction result. raw=" + raw, e);
}
```

问题是：

```text
1. 模型可能返回 Markdown
2. 模型可能返回解释文字
3. 模型可能漏字段
4. priority 可能返回“高”而不是 HIGH
5. JSON 可能格式错误
6. 报错信息不够清晰
7. 没有自动修复
```

---

## 本课要改哪些文件？

主要改：

```text
TaskExtractionService.java
```

建议新增：

```text
exception/AiStructuredOutputException.java
```

可选新增：

```text
dto/StructuredOutputErrorCode.java
```

本课先保持简单，不做过度设计。
