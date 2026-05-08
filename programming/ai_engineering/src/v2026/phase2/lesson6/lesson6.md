# 第 6 课：Function Calling / Tool Calling

## 本课要解决什么问题

前面第 4、5 课解决的是：

```text
自然语言 -> 结构化 DTO
```

比如：

```json
{
  "taskName": "给张三发报价单",
  "dueTimeText": "明天下午三点",
  "priority": "HIGH",
  "assignee": "me"
}
```

但真实 AI 应用不只是“抽取信息”，还要能**调用后端能力**。

例如用户问：

```text
帮我查一下订单 10086 的状态。
```

模型不应该自己编一个订单状态，而应该判断：

```text
这个问题需要调用订单查询工具。
```

然后生成工具调用参数：

```json
{
  "toolName": "getOrderStatus",
  "arguments": {
    "orderId": "10086"
  }
}
```

Java 后端再真正执行：

```text
getOrderStatus("10086")
```

最终返回：

```text
订单 10086 当前状态是：已发货，预计明天送达。
```

一句话概括本课：

> 本课要让模型从“只会回答”升级为“能判断是否需要调用后端工具，并生成安全可执行的工具参数”。

## 本课要新增的接口

新增接口：

```http
POST /api/ai/order-assistant
```

请求：

```json
{
  "message": "帮我查一下订单 10086 的状态"
}
```

响应：

```json
{
  "answer": "订单 10086 当前状态是：已发货，预计明天送达。"
}
```

## 本课调用链

```text
OrderAssistantController
  -> OrderAssistantService
  -> LlmClient.complete
  -> 模型判断是否调用工具
  -> ToolCallDecision
  -> OrderToolService.getOrderStatus
  -> 返回最终回答
```

## 本课工具调用策略

本课先不用模型供应商原生 function calling，而是继续用你已经掌握的方式：

```text
Prompt 约束 + JSON 输出 + Jackson 解析 + Java 执行工具
```

原因：

1. 你正在学习底层原理。
2. OpenAI-compatible 平台对 tool calling 支持不完全一致。
3. 先手写可以理解 tool calling 的本质。
4. 后续再升级到原生 tool calling 会更容易。
