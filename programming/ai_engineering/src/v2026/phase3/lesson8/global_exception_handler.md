# 修改 GlobalExceptionHandler

增加两个异常处理。

```java
import com.example.aigateway.exception.LlmFallbackException;
import com.example.aigateway.exception.LlmRateLimitException;
```

在 `GlobalExceptionHandler` 中新增：

```java
@ExceptionHandler(LlmRateLimitException.class)
@ResponseStatus(HttpStatus.TOO_MANY_REQUESTS)
public ErrorResponse handleLlmRateLimitException(LlmRateLimitException e) {
    return new ErrorResponse(
            "LLM_RATE_LIMITED",
            e.getMessage(),
            Instant.now().toString()
    );
}

@ExceptionHandler(LlmFallbackException.class)
@ResponseStatus(HttpStatus.BAD_GATEWAY)
public ErrorResponse handleLlmFallbackException(LlmFallbackException e) {
    return new ErrorResponse(
            "LLM_FALLBACK",
            e.getMessage(),
            Instant.now().toString()
    );
}
```
