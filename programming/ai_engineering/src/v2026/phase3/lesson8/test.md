# 测试

## 正常调用聊天接口

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"请用一句话解释什么是 RAG"}'
```

预期：正常返回。

---

## 查询日志确认成功记录

```bash
curl http://localhost:8080/api/ai/llm-call-logs
```

应该看到 `success: true` 的调用记录。

---

## 测试限流

把 `LlmRateLimiter` 里的：

```java
private static final int MAX_REQUESTS_PER_MINUTE = 30;
```

临时改成：

```java
private static final int MAX_REQUESTS_PER_MINUTE = 2;
```

然后连续快速调用 3 次：

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

测试完成后记得改回：

```java
private static final int MAX_REQUESTS_PER_MINUTE = 30;
```

---

## 测试 fallback

临时把 `application.yml` 里的模型名改错，例如：

```yaml
model: wrong-model-name
```

然后调用：

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"hello"}'
```

预期返回：

```json
{
  "code": "LLM_FALLBACK",
  "message": "LLM provider is temporarily unavailable. Please try again later.",
  "timestamp": "..."
}
```

注意：模型名错误理论上不适合重试，但会进入 fallback 错误处理。
