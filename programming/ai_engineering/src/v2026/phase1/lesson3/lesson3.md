# 第 3 课：实现流式输出接口

本课目标：

```text
POST /api/ai/chat/stream
```

让模型回答可以逐步返回：

```text
R
RA
RAG
RAG 是
RAG 是一种...
```

实际前端展示时就是“打字机效果”。

## 今天要完成的接口

新增接口：

```http
POST /api/ai/chat/stream
Content-Type: application/json
Accept: text/event-stream
```

请求：

```json
{
  "message": "请解释一下什么是 RAG"
}
```

响应不是普通 JSON，而是 SSE 流：

```text
data: RAG

data: 是一种

data: 检索增强生成

data: 技术
```
