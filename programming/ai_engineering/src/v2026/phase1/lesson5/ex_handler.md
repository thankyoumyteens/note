# 增强全局异常处理

修改 `GlobalExceptionHandler.java`，增加对 `AiStructuredOutputException` 的处理。

文件：

```text
src/main/java/com/example/aigateway/controller/GlobalExceptionHandler.java
```

```java
package com.example.aigateway.controller;

import com.example.aigateway.exception.AiStructuredOutputException;
import java.time.Instant;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

/**
 * 全局异常处理器。
 *
 * 作用：
 * - 不把 Java 异常堆栈直接暴露给前端
 * - 统一错误响应格式
 * - 为后续错误分类打基础
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * 处理用户请求参数错误。
     */
    @ExceptionHandler(IllegalArgumentException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handleIllegalArgumentException(IllegalArgumentException e) {
        return new ErrorResponse(
                "BAD_REQUEST",
                e.getMessage(),
                Instant.now().toString()
        );
    }

    /**
     * 处理 AI 结构化输出失败。
     *
     * 注意：
     * 这里不要把 rawOutput 返回给前端。
     */
    @ExceptionHandler(AiStructuredOutputException.class)
    @ResponseStatus(HttpStatus.BAD_GATEWAY)
    public ErrorResponse handleAiStructuredOutputException(AiStructuredOutputException e) {
        // 学习阶段可以先打印，生产环境应替换为正式日志框架。
        System.err.println("AI structured output error: " + e.getMessage());
        System.err.println("AI raw output: " + e.getRawOutput());

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
