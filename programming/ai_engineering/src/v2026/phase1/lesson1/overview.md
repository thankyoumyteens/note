# 第 1 阶段我们要做什么？

我们先做 4 个小模块。

## 模块 1：普通聊天接口

接口：

```http
POST /api/ai/chat
```

请求：

```json
{
  "message": "请用一句话解释什么是 RAG"
}
```

响应：

```json
{
  "answer": "RAG 是一种让大模型先检索外部知识，再基于检索结果回答问题的技术。"
}
```

目标：你能从 Java 后端调用模型。

---

## 模块 2：流式输出接口

接口：

```http
POST /api/ai/chat/stream
```

效果类似 ChatGPT，一个字一个字输出。

目标：掌握 SSE / WebFlux / streaming。

---

## 模块 3：结构化输出接口

接口：

```http
POST /api/ai/extract-task
```

请求：

```json
{
  "text": "明天下午三点提醒我给张三发报价单，优先级高。"
}
```

响应：

```json
{
  "taskName": "给张三发报价单",
  "dueTime": "明天下午三点",
  "priority": "high",
  "assignee": "me"
}
```

目标：模型输出能被 Java DTO 稳定接收。

---

## 模块 4：工具调用接口

接口：

```http
POST /api/ai/order-assistant
```

请求：

```json
{
  "message": "帮我查订单 10086 的状态"
}
```

模型判断要调用工具：

```text
getOrderStatus(orderId=10086)
```

Java 后端执行工具后返回：

```json
{
  "answer": "订单 10086 当前状态是：已发货，预计明天送达。"
}
```

目标：理解 Agent 的第一层原理。
