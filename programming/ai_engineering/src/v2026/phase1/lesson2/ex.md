# 现在加一个全局异常处理

目前如果模型调用失败，Spring 会返回默认错误页或默认 JSON，不够清晰。

新建：

```text
controller/GlobalExceptionHandler.java
```

代码：

```java
package com.example.aigateway.controller;

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

现在如果 API Key 错了、模型名错了、网络失败，至少会返回清楚的错误信息。
