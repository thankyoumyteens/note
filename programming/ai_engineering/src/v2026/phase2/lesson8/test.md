# 测试方式

### 5.1 测试普通聊天日志

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"请用一句话解释什么是 RAG"}'
```

然后查询：

```bash
curl http://localhost:8080/api/ai/llm-call-logs
```

应该看到：

```json
{
  "callType": "CHAT",
  "model": "...",
  "success": true,
  "latencyMs": 1234,
  "totalTokens": 123
}
```

---

### 5.2 测试任务抽取日志

```bash
curl -X POST http://localhost:8080/api/ai/extract-task \
  -H "Content-Type: application/json" \
  --data-raw '{"text":"明天下午三点提醒我给张三发报价单，优先级高。"}'
```

查询：

```bash
curl http://localhost:8080/api/ai/llm-call-logs
```

应该看到：

```text
TASK_EXTRACTION
```

如果触发修复，还会看到：

```text
JSON_REPAIR
```

---

### 5.3 测试工具调用日志

```bash
curl -X POST http://localhost:8080/api/ai/order-assistant \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"帮我查一下订单 10086 的状态"}'
```

查询：

```bash
curl http://localhost:8080/api/ai/tool-call-logs
```

应该看到类似：

```json
{
  "shouldCallTool": true,
  "toolName": "getOrderStatus",
  "argumentsJson": "{\"orderId\":\"10086\"}",
  "toolResult": "订单 10086 当前状态是：已发货，预计明天送达。",
  "success": true
}
```

---

### 5.4 测试限流

临时把：

```java
private static final int MAX_REQUESTS_PER_MINUTE = 30;
```

改成：

```java
private static final int MAX_REQUESTS_PER_MINUTE = 2;
```

连续调用 3 次：

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"test"}'
```

第三次应该返回：

```json
{
  "code": "LLM_RATE_LIMITED",
  "message": "Too many LLM requests. Please try again later.",
  "timestamp": "..."
}
```

测试后改回 30。

---

### 5.5 测试 fallback

临时把 `application.yml` 里的模型名改错：

```yaml
model: wrong-model-name
```

调用：

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"hello"}'
```

预期：

```json
{
  "code": "LLM_FALLBACK",
  "message": "LLM provider is temporarily unavailable. Please try again later.",
  "timestamp": "..."
}
```

测试后恢复模型名。
