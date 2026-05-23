# 新增 LlmCallLog

模型计费通常和 token 有关。

需要记录：

```text
promptTokens
completionTokens
totalTokens
```

含义：

```text
promptTokens：输入消耗
completionTokens：输出消耗
totalTokens：总消耗
```

这为后续成本统计打基础。

## 代码实现

文件：

```text
src/main/java/com/example/aigateway/dto/LlmCallLog.java
```

```java
package com.example.aigateway.dto;

import java.time.Instant;
import java.util.UUID;

/**
 * 大模型调用日志。
 *
 * 注意：
 * 当前不记录完整 prompt，避免泄露用户隐私或内部 system prompt。
 */
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
    public static LlmCallLog success(
            LlmCallType callType,
            String model,
            long latencyMs,
            Integer promptTokens,
            Integer completionTokens,
            Integer totalTokens
    ) {
        return new LlmCallLog(
                UUID.randomUUID().toString(),
                callType,
                model,
                true,
                latencyMs,
                promptTokens,
                completionTokens,
                totalTokens,
                null,
                Instant.now()
        );
    }

    public static LlmCallLog failure(
            LlmCallType callType,
            String model,
            long latencyMs,
            String errorMessage
    ) {
        return new LlmCallLog(
                UUID.randomUUID().toString(),
                callType,
                model,
                false,
                latencyMs,
                null,
                null,
                null,
                errorMessage,
                Instant.now()
        );
    }
}
```
