# 核心概念

## 什么是 Function Calling / Tool Calling？

Function Calling，也叫 Tool Calling，核心思想是：

```text
模型负责判断要不要调用工具，以及生成工具参数；
后端负责真正执行工具。
```

模型本身不会真的查数据库、调用接口、发邮件、改订单。

它只是输出类似这样的结构化结果：

```json
{
  "toolName": "getOrderStatus",
  "arguments": {
    "orderId": "10086"
  }
}
```

真正执行的是 Java 后端。

所以要记住：

```text
模型不执行工具。
模型只是提出工具调用意图。
后端才执行工具。
```

## 什么是 Tool？

Tool 就是后端暴露给模型使用的能力。

例如：

```text
getOrderStatus(orderId)
searchKnowledgeBase(query)
createTicket(title, description)
sendEmail(to, subject, body)
queryUserProfile(userId)
```

本课先做一个最简单的工具：

```text
getOrderStatus(orderId)
```

它的职责是根据订单号返回订单状态。

为了避免复杂数据库，本课先用 Mock 数据。

---

## 什么是 Tool Schema？

Tool Schema 是工具说明书。

它告诉模型：

```text
有哪些工具可以用
每个工具叫什么
每个工具能做什么
每个工具需要哪些参数
参数类型是什么
哪些参数必填
```

例如：

```json
{
  "name": "getOrderStatus",
  "description": "根据订单号查询订单状态",
  "parameters": {
    "orderId": "订单号，字符串"
  }
}
```

模型看到这个说明后，才知道：

```text
当用户问订单状态时，应该调用 getOrderStatus。
```
