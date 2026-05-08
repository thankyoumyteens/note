# 第 4 课：结构化输出 Structured Output

本课目标是让 AI Gateway 从“返回自然语言文本”升级为“返回 Java 业务系统可以稳定消费的结构化 DTO”。

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

## 结构化输出在 AI 应用中的地位

结构化输出是 AI 应用开发的核心能力之一。

很多 AI 应用不是简单问答，而是：

```text
自然语言输入 -> 结构化业务对象
```

典型场景：

- 任务抽取
- 邮件信息抽取
- 工单分类
- 意图识别
- 合同字段抽取
- 发票解析
- 简历解析
- 客服对话标签
- SQL 生成参数
- 工具调用参数生成

例如：

```text
“帮我查一下订单 10086 的物流状态”
```

需要变成：

```json
{
  "intent": "QUERY_ORDER_STATUS",
  "orderId": "10086"
}
```

后端才能判断要调用哪个工具。

所以结构化输出也是后续 Function Calling / Tool Calling 的前置能力。

## 先做 Prompt 约束版

2026 年很多主流模型已经支持原生结构化输出，例如 JSON Schema、response_format、tool schema 等。

但本课先使用：

```text
Prompt 约束 + Jackson 解析 + Java DTO 校验
```

原因：

1. OpenAI-compatible 平台不一定都支持原生 JSON Schema。
2. 先理解结构化输出的底层工程逻辑。
3. 后续 Function Calling 本质上也会涉及 JSON 参数解析。
4. 先自己处理一次，才能理解为什么生产系统需要强约束和校验。

本课不是最终方案，而是基础方案。

当前策略：

```text
先用 Prompt 要求模型输出 JSON
再用 Jackson 解析为 Java DTO
最后做字段规范化
```

## Prompt 约束不是强约束

这一点非常重要。

即使 Prompt 写了：

```text
只能输出 JSON
```

模型仍然可能返回：

```text
好的，以下是提取结果：
{
  "taskName": "给张三发报价单",
  ...
}
```

或者：

````text
```json
{
  "taskName": "给张三发报价单"
}
```
````

或者返回不合法 JSON：

```text
{
  "taskName": "给张三发报价单",
  "priority": "高",
}
```

所以后端不能直接信任模型输出。

本课先做基础清理，第 5 课再加入自动修复和错误分类。
