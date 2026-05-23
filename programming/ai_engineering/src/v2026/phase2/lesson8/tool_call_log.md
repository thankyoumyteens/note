# 新增 ToolCallLog

文件：

```text
src/main/java/com/example/aigateway/dto/ToolCallLog.java
```

```java
package com.example.aigateway.dto;

import java.time.Instant;
import java.util.UUID;

/**
 * 工具调用决策与执行日志。
 *
 * 用于记录模型是否决定调用工具、调用哪个工具、参数是什么、执行结果如何。
 */
public record ToolCallLog(
        String id,
        boolean shouldCallTool,
        String toolName,
        String argumentsJson,
        String toolResult,
        boolean success,
        long latencyMs,
        String errorMessage,
        Instant createdAt
) {
    public static ToolCallLog of(
            boolean shouldCallTool,
            String toolName,
            String argumentsJson,
            String toolResult,
            boolean success,
            long latencyMs,
            String errorMessage
    ) {
        return new ToolCallLog(
                UUID.randomUUID().toString(),
                shouldCallTool,
                toolName,
                argumentsJson,
                toolResult,
                success,
                latencyMs,
                errorMessage,
                Instant.now()
        );
    }
}
```
