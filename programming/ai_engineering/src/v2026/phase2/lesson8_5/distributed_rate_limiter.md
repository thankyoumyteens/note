# 新增 DistributedRateLimiter

定义分布式限流器抽象，让业务代码不直接绑定 Redis。

和 `LlmClient` 一样，限流也应该有接口抽象。

当前实现是 Redis，未来可能换成：

```text
Bucket4j
Sentinel
Envoy Rate Limit Service
API Gateway 限流
```

所以业务层依赖 `DistributedRateLimiter`，不要直接依赖 `RedisRateLimiter`。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/service/DistributedRateLimiter.java
```

代码：

```java
package com.example.aigateway.service;

import com.example.aigateway.dto.RateLimitRequest;
import com.example.aigateway.dto.RateLimitResult;

/**
 * 分布式限流器抽象。
 *
 * 为什么要有接口：
 * - 当前可以使用 Redis 实现
 * - 后续可以替换为 Bucket4j、Sentinel、Envoy RLS、网关层限流等方案
 */
public interface DistributedRateLimiter {

    /**
     * 尝试获取调用许可。
     *
     * 如果 allowed=false，调用方应该拒绝请求。
     */
    RateLimitResult acquire(RateLimitRequest request);
}
```

#### 代码说明

`acquire` 表示“尝试获取调用资格”。

返回：

```text
allowed = true：可以继续调用模型
allowed = false：应该拒绝请求
```
