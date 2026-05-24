# 测试方式

## 查询限流状态

```bash
curl http://localhost:8080/api/ai/rate-limit-status
```

预期：

```json
{
  "enabled": true,
  "mode": "redis-fixed-window",
  "description": "Redis distributed rate limiter is configured for AI Gateway."
}
```

---

## 测试正常模型调用

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"请用一句话解释什么是 RAG"}'
```

预期：正常返回模型回答。

---

## 测试触发限流

临时把配置改小：

```yaml
ai:
  rate-limit:
    enabled: true
    default-rule:
      limit: 2
      window-seconds: 60
    call-type-rules:
      CHAT:
        limit: 2
        window-seconds: 60
```

重启服务后，连续调用 3 次：

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  --data-raw '{"message":"test"}'
```

第 3 次预期：

```json
{
  "code": "LLM_RATE_LIMITED",
  "message": "Too many LLM requests. Please try again later. key=..., current=..., limit=..., retryAfterSeconds=...",
  "timestamp": "..."
}
```

测试完成后，把 limit 改回正常值。

---

## 查看 Redis key

```bash
redis-cli keys 'ai-gateway:rate-limit:*'
```

可能看到：

```text
ai-gateway:rate-limit:global
ai-gateway:rate-limit:call-type:CHAT
ai-gateway:rate-limit:model:gpt-4o-mini
```

查看 TTL：

```bash
redis-cli ttl ai-gateway:rate-limit:call-type:CHAT
```

查看计数：

```bash
redis-cli get ai-gateway:rate-limit:call-type:CHAT
```
