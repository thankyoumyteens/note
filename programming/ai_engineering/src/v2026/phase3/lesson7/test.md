# 测试

## 调用普通聊天

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"请用一句话解释什么是 RAG"}'
```

---

## 6.2 调用任务抽取

```bash
curl -X POST http://localhost:8080/api/ai/extract-task \
  -H "Content-Type: application/json" \
  --data-raw '{"text":"明天下午三点提醒我给张三发报价单，优先级高。"}'
```

---

## 6.3 调用订单助手

```bash
curl -X POST http://localhost:8080/api/ai/order-assistant \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"帮我查一下订单 10086 的状态"}'
```

---

## 6.4 查询调用日志

```bash
curl http://localhost:8080/api/ai/llm-call-logs
```

预期返回类似：

```json
[
  {
    "id": "xxx",
    "callType": "TOOL_DECISION",
    "model": "gpt-xxx",
    "success": true,
    "latencyMs": 1200,
    "promptTokens": 300,
    "completionTokens": 60,
    "totalTokens": 360,
    "errorMessage": null,
    "createdAt": "2026-05-08T..."
  }
]
```

你应该能看到：

```text
CHAT
TASK_EXTRACTION
TOOL_DECISION
JSON_REPAIR
STREAM_CHAT
```

不同类型的日志。
