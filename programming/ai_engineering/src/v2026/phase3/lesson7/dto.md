# 新增调用日志 DTO

新建：

```text
dto/LlmCallLog.java
```

```java
package com.example.aigateway.dto;

import java.time.Instant;

public record LlmCallLog(
        String id,
        LlmCallType callType,
        String model,
        boolean success,
        long latencyMs,
        Integer promptTokens,
        Integer completionTokens,
        Integer totalTokens,
        String errorMessage,
        Instant createdAt
) {
}
```

说明：

```text
Integer 而不是 int，是因为流式输出或异常情况下可能没有 token usage。
```
