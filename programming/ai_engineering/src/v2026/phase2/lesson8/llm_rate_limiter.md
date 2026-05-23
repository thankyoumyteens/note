# 新增 LlmRateLimiter

## 为什么需要限流

AI 接口比普通接口更需要限流。

原因：

```text
模型调用成本高
模型调用慢
容易被刷爆
供应商也有限流
线程资源会被长请求占用
```

本课先做内存限流：

```text
每分钟最多 N 次模型调用
```

生产系统后续可换成 Redis / API Gateway / Envoy / Nginx。

## 代码实现

文件：

```text
src/main/java/com/example/aigateway/service/LlmRateLimiter.java
```

```java
package com.example.aigateway.service;

import com.example.aigateway.exception.LlmRateLimitException;
import java.time.Instant;
import java.util.ArrayDeque;
import java.util.Deque;
import org.springframework.stereotype.Service;

/**
 * 简单内存版限流器。
 *
 * 当前策略：
 * - 全局每分钟最多 30 次模型调用
 *
 * 生产环境应替换为 Redis / API Gateway / 分布式限流。
 */
@Service
public class LlmRateLimiter {

    private static final int MAX_REQUESTS_PER_MINUTE = 30;
    private static final long WINDOW_MILLIS = 60_000;

    private final Deque<Long> requestTimestamps = new ArrayDeque<>();

    public synchronized void acquire() {
        long now = Instant.now().toEpochMilli();

        while (!requestTimestamps.isEmpty()
                && now - requestTimestamps.peekFirst() > WINDOW_MILLIS) {
            requestTimestamps.removeFirst();
        }

        if (requestTimestamps.size() >= MAX_REQUESTS_PER_MINUTE) {
            throw new LlmRateLimitException("Too many LLM requests. Please try again later.");
        }

        requestTimestamps.addLast(now);
    }
}
```
