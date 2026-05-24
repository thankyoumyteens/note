# 修改 LlmRateLimitException

让限流异常携带 key、当前计数、限制和剩余时间，方便调试。

生产环境不一定把这些细节返回给用户，但学习阶段返回出来更容易理解限流是怎么触发的。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/exception/LlmRateLimitException.java
```

代码：

```java
package com.example.aigateway.exception;

/**
 * AI Gateway 限流异常。
 */
public class LlmRateLimitException extends RuntimeException {

    private final String key;
    private final long current;
    private final long limit;
    private final long ttlSeconds;

    public LlmRateLimitException(
            String message,
            String key,
            long current,
            long limit,
            long ttlSeconds
    ) {
        super(message);
        this.key = key;
        this.current = current;
        this.limit = limit;
        this.ttlSeconds = ttlSeconds;
    }

    public String getKey() {
        return key;
    }

    public long getCurrent() {
        return current;
    }

    public long getLimit() {
        return limit;
    }

    public long getTtlSeconds() {
        return ttlSeconds;
    }
}
```

别忘了直接删除旧的：LlmRateLimiter.java，避免报错。
