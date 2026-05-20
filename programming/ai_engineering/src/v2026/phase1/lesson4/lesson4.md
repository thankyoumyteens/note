# 第 4 课：结构化输出 Structured Output

本课目标是让 AI Gateway 从“返回自然语言文本”升级为“返回 Java 业务系统可以稳定消费的结构化 DTO”。

本课目标是让 AI Gateway 不只返回自然语言，而是能够把用户输入抽取成 Java 后端可以稳定消费的结构化 DTO。

之前的接口返回：

```json
{
  "answer": "用户想明天下午三点给张三发报价单，优先级比较高。"
}
```

这适合人读，但不适合程序处理。

本课要实现：

```http
POST /api/ai/extract-task
```

把用户输入：

```json
{
  "text": "明天下午三点提醒我给张三发报价单，优先级高。"
}
```

抽取成：

```json
{
  "taskName": "给张三发报价单",
  "dueTimeText": "明天下午三点",
  "priority": "HIGH",
  "assignee": "me"
}
```

一句话概括：

> 本课实现一个任务信息抽取接口，用 Prompt 约束模型输出 JSON，再用 Jackson 解析成 Java DTO。

OpenAI 官方的 Structured Outputs 是让模型输出严格符合 JSON Schema 的能力；本课先不用原生 JSON Schema，而是先用“Prompt 约束 + Jackson 解析”的基础方案，目的是理解结构化输出底层工程逻辑。

## 结构化输出在 AI 应用中的地位

自然语言输出适合人看，但后端系统需要明确字段。

例如用户输入：

```text
明天下午三点提醒我给张三发报价单，优先级高。
```

模型自然语言回答可能是：

```text
用户想在明天下午三点给张三发报价单，这是一个高优先级任务。
```

这段话人能理解，但程序很难稳定处理。

后端更需要：

```json
{
  "taskName": "给张三发报价单",
  "dueTimeText": "明天下午三点",
  "priority": "HIGH",
  "assignee": "me"
}
```

这样 Java 可以直接反序列化成 DTO，然后继续做业务处理。

## Prompt 约束不是强约束

这一点非常重要。

即使 Prompt 写了：

```text
只能输出 JSON
```

模型仍然可能返回：

````text
```json
{
  "taskName": "给张三发报价单"
}
```
````

或者：

```text
好的，以下是提取结果：
{
  "taskName": "给张三发报价单"
}
```

所以后端不能直接信任模型输出。

本课先做基础清理，第 5 课再加入自动修复和错误分类。
