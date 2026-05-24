# 修改 GlobalExceptionHandler

让限流失败时返回统一错误码 `LLM_RATE_LIMITED`。

限流属于可预期的业务保护，不应该直接返回 500。

更合适的 HTTP 状态码是：

```text
429 Too Many Requests
```

#### 代码

把 `handleLlmRateLimitException`，改成：

```java
@ExceptionHandler(LlmRateLimitException.class)
@ResponseStatus(HttpStatus.TOO_MANY_REQUESTS)
public ErrorResponse handleLlmRateLimitException(LlmRateLimitException e) {
    return new ErrorResponse(
            "LLM_RATE_LIMITED",
            e.getMessage()
                    + " key=" + e.getKey()
                    + ", current=" + e.getCurrent()
                    + ", limit=" + e.getLimit()
                    + ", retryAfterSeconds=" + e.getTtlSeconds(),
            Instant.now().toString()
    );
}
```

#### 代码说明

学习阶段返回限流细节，方便确认：

```text
哪个 key 被限流
当前计数是多少
上限是多少
多久后恢复
```

生产环境可以隐藏 `key`，只返回简短提示。
