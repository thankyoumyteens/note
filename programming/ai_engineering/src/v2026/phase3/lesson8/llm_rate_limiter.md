# 新增限流组件

职责：

- 记录最近一分钟的模型调用次数
- 超过限制时拒绝请求

新建：

```text
service/LlmRateLimiter.java
```

```java
package com.example.aigateway.service;

import com.example.aigateway.exception.LlmRateLimitException;
import java.time.Instant;
import java.util.ArrayDeque;
import java.util.Deque;
import org.springframework.stereotype.Service;

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

说明：

```text
这是全局内存限流。
服务重启后计数清零。
多实例部署时不共享状态。
```

当前学习阶段够用。
