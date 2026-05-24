# 新增 RateLimitResult

返回限流判断结果，并携带调试信息。

限流结果不能只返回 `true/false`。为了调试和错误响应，最好知道：

```text
哪个 key 被限流
当前计数是多少
限制是多少
还要等多久
```

#### 代码

文件：

```text
src/main/java/com/example/aigateway/dto/RateLimitResult.java
```

代码：

```java
package com.example.aigateway.dto;

/**
 * 限流判断结果。
 */
public record RateLimitResult(
        boolean allowed,
        String key,
        long current,
        long limit,
        long ttlSeconds
) {
    public static RateLimitResult allowed(
            String key,
            long current,
            long limit,
            long ttlSeconds
    ) {
        return new RateLimitResult(
                true,
                key,
                current,
                limit,
                ttlSeconds
        );
    }

    public static RateLimitResult rejected(
            String key,
            long current,
            long limit,
            long ttlSeconds
    ) {
        return new RateLimitResult(
                false,
                key,
                current,
                limit,
                ttlSeconds
        );
    }
}
```

#### 代码说明

字段含义：

```text
allowed：是否允许
key：Redis 限流 key
current：当前窗口内已经调用多少次
limit：允许上限
ttlSeconds：当前窗口还有多少秒过期
```
