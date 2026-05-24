# 新增 RateLimitKeyResolver

统一生成 Redis 限流 key，避免 key 散落在业务代码里。

限流的核心不是只有算法，还有 key 设计。

例如：

```text
全局限流：ai-gateway:rate-limit:global
按调用类型：ai-gateway:rate-limit:call-type:CHAT
按模型：ai-gateway:rate-limit:model:gpt-4o-mini
```

key 设计决定了限流维度。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/service/RateLimitKeyResolver.java
```

代码：

```java
package com.example.aigateway.service;

import com.example.aigateway.dto.RateLimitRequest;
import org.springframework.stereotype.Service;

/**
 * 限流 Key 生成器。
 *
 * 生产级限流的关键不是只有算法，
 * 还要设计清楚“按什么维度限流”。
 *
 * 当前先支持：
 * - 全局限流 key
 * - 按 callType 限流 key
 * - 按 model 限流 key
 */
@Service
public class RateLimitKeyResolver {

    private static final String PREFIX = "ai-gateway:rate-limit";

    /**
     * 全局限流 key。
     */
    public String globalKey() {
        return PREFIX + ":global";
    }

    /**
     * 按 callType 限流。
     */
    public String callTypeKey(RateLimitRequest request) {
        return PREFIX + ":call-type:" + request.callType().name();
    }

    /**
     * 按模型限流。
     */
    public String modelKey(RateLimitRequest request) {
        String model = request.model() == null || request.model().isBlank()
                ? "unknown"
                : request.model().strip();

        return PREFIX + ":model:" + model;
    }

    /**
     * 后续可扩展：按租户限流。
     */
    public String tenantKey(RateLimitRequest request) {
        String tenantId = request.tenantId() == null || request.tenantId().isBlank()
                ? "default"
                : request.tenantId().strip();

        return PREFIX + ":tenant:" + tenantId;
    }

    /**
     * 后续可扩展：按用户限流。
     */
    public String userKey(RateLimitRequest request) {
        String userId = request.userId() == null || request.userId().isBlank()
                ? "anonymous"
                : request.userId().strip();

        return PREFIX + ":user:" + userId;
    }
}
```

本课实际使用：

```text
globalKey
callTypeKey
modelKey
```

`tenantKey` 和 `userKey` 先保留扩展点，不接真实权限系统。
