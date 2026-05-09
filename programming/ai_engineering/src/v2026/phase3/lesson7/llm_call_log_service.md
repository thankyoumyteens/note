# 新增日志 Service

先用内存保存最近 100 条调用记录。

新建：

```text
service/LlmCallLogService.java
```

```java
package com.example.aigateway.service;

import com.example.aigateway.dto.LlmCallLog;
import com.example.aigateway.dto.LlmCallType;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import org.springframework.stereotype.Service;

@Service
public class LlmCallLogService {

    private static final int MAX_SIZE = 100;

    private final List<LlmCallLog> logs = new ArrayList<>();

    public synchronized void recordSuccess(
            LlmCallType callType,
            String model,
            long latencyMs,
            Integer promptTokens,
            Integer completionTokens,
            Integer totalTokens
    ) {
        addLog(new LlmCallLog(
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
        ));
    }

    public synchronized void recordFailure(
            LlmCallType callType,
            String model,
            long latencyMs,
            String errorMessage
    ) {
        addLog(new LlmCallLog(
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
        ));
    }

    public synchronized List<LlmCallLog> findRecent() {
        return logs.reversed();
    }

    private void addLog(LlmCallLog log) {
        logs.add(log);

        if (logs.size() > MAX_SIZE) {
            logs.remove(0);
        }
    }
}
```

如果你的 Java 环境不支持 `logs.reversed()`，改成：

```java
public synchronized List<LlmCallLog> findRecent() {
    List<LlmCallLog> copy = new ArrayList<>(logs);
    java.util.Collections.reverse(copy);
    return copy;
}
```

Java 21 支持 `List#reversed()`，但如果编译报错，就用兼容写法。
