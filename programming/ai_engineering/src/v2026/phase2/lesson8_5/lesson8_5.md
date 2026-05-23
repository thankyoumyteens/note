# 第 8.5 课：生产级限流与网关治理

第 8 课的 `LlmRateLimiter` 是单机内存限流器，只适合本地学习。生产环境通常会部署多个 `ai-gateway` 实例，如果每个实例各自限流，就无法保证全局限流一致。

一句话概括：

> 本课把单机内存限流升级为 Redis 分布式限流，让多个 AI Gateway 实例共享同一套限流计数。

## 本课最终效果

当前第 8 课调用链大概是：

```text
OpenAiCompatibleLlmClient
  -> LlmRateLimiter
  -> 内存 Deque
```

本课完成后变成：

```text
OpenAiCompatibleLlmClient
  -> DistributedRateLimiter
  -> RedisRateLimiter
  -> Redis
```

新增能力：

```text
1. 多实例共享限流计数
2. 支持按 callType 限流
3. 支持按 model 设计限流 key
4. 保留 LLM_RATE_LIMITED 统一错误响应
5. 可以通过 Redis 查看限流 key 和 TTL
```

新增调试接口：

```http
GET /api/ai/rate-limit-status
```
