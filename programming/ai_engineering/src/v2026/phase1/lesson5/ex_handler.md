# 增强全局异常处理

修改 `GlobalExceptionHandler.java`，增加对 `AiStructuredOutputException` 的处理。

```java
package com.example.aigateway.controller;

import com.example.aigateway.exception.AiStructuredOutputException;
import java.time.Instant;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(IllegalArgumentException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handleIllegalArgumentException(IllegalArgumentException e) {
        return new ErrorResponse(
                "BAD_REQUEST",
                e.getMessage(),
                Instant.now().toString()
        );
    }

    @ExceptionHandler(AiStructuredOutputException.class)
    @ResponseStatus(HttpStatus.BAD_GATEWAY)
    public ErrorResponse handleAiStructuredOutputException(AiStructuredOutputException e) {
        return new ErrorResponse(
                "AI_STRUCTURED_OUTPUT_ERROR",
                e.getMessage(),
                Instant.now().toString()
        );
    }

    @ExceptionHandler(RuntimeException.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ErrorResponse handleRuntimeException(RuntimeException e) {
        return new ErrorResponse(
                "INTERNAL_ERROR",
                e.getMessage(),
                Instant.now().toString()
        );
    }

    public record ErrorResponse(
            String code,
            String message,
            String timestamp
    ) {
    }
}
```

注意：这里不要把 `rawOutput` 直接返回给用户。
原始模型输出可以打日志，但不要暴露给外部调用方。
