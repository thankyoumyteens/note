# 修改 OpenAiCompatibleLlmClient

把第 8 课的单机内存限流替换成 Redis 分布式限流。

这里体现一个重要工程边界：

```text
OpenAiCompatibleLlmClient 不关心限流底层是内存、Redis、Sentinel 还是网关。
它只依赖 DistributedRateLimiter。
```

#### 代码

把原来的：

```java
private final LlmRateLimiter llmRateLimiter;
```

替换为：

```java
private final DistributedRateLimiter distributedRateLimiter;
```

构造器改成：

```java
public OpenAiCompatibleLlmClient(
        WebClient llmWebClient,
        LlmProperties properties,
        ObjectMapper objectMapper,
        LlmCallLogService llmCallLogService,
        DistributedRateLimiter distributedRateLimiter
) {
    this.llmWebClient = llmWebClient;
    this.properties = properties;
    this.objectMapper = objectMapper;
    this.llmCallLogService = llmCallLogService;
    this.distributedRateLimiter = distributedRateLimiter;
}
```

在 `complete(...)` 开头，把：

```java
llmRateLimiter.acquire();
```

替换为：

```java
acquireRateLimit(callType);
```

在 `streamChat(...)` 开头，把：

```java
llmRateLimiter.acquire();
```

替换为：

```java
acquireRateLimit(LlmCallType.STREAM_CHAT);
```

新增方法：

```java
/**
 * 执行分布式限流。
 *
 * 当前基于：
 * - callType
 * - model
 *
 * 后续可以扩展：
 * - userId
 * - tenantId
 * - apiKey
 * - ip
 */
private void acquireRateLimit(LlmCallType callType) {
    RateLimitResult result = distributedRateLimiter.acquire(
            RateLimitRequest.forLlmCall(
                    callType,
                    properties.getModel()
            )
    );

    if (!result.allowed()) {
        throw new LlmRateLimitException(
                "Too many LLM requests. Please try again later.",
                result.key(),
                result.current(),
                result.limit(),
                result.ttlSeconds()
        );
    }
}
```

需要 import：

```java
import com.example.aigateway.dto.RateLimitRequest;
import com.example.aigateway.dto.RateLimitResult;
import com.example.aigateway.exception.LlmRateLimitException;
import com.example.aigateway.service.DistributedRateLimiter;
```
