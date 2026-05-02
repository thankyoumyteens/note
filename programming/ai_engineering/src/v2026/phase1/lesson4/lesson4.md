# 第 4 课：结构化输出 Structured Output

前面你已经完成：

```text
/api/ai/chat         普通回答
/api/ai/chat/stream  流式回答
```

现在进入更重要的一步：

```text
/api/ai/extract-task
```

让模型不要返回一段自然语言，而是返回**业务系统可以稳定处理的 JSON / DTO**。

OpenAI 官方把 Structured Outputs 定义为：让模型响应遵循你提供的 JSON Schema，避免漏字段或生成非法枚举值；Spring AI 也提供了 `StructuredOutputConverter`，用于把模型文本输出转换成 Java 类、数组或其他结构化对象。

---

## 本课目标

输入一句自然语言：

```json
{
  "text": "明天下午三点提醒我给张三发报价单，优先级高。"
}
```

输出结构化 JSON：

```json
{
  "taskName": "给张三发报价单",
  "dueTimeText": "明天下午三点",
  "priority": "HIGH",
  "assignee": "me"
}
```

这一步非常关键，因为真实业务系统不能稳定消费这种输出：

```text
用户想让我明天下午三点提醒他给张三发报价单，看起来优先级比较高。
```

后端需要的是：

```java
TaskExtractionResult result
```

而不是一段自然语言。

---

## 先做 Prompt 约束版

这一课我们先不用模型原生 JSON Schema，而是用：

```text
Prompt 约束 + Jackson 解析 + Java DTO 校验
```

原因是：

1. OpenAI-compatible 平台不一定都支持原生 `response_format: json_schema`。
2. 先理解结构化输出的底层工程逻辑。
3. 后面再升级成原生 Structured Outputs。
