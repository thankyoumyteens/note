# 新增 LlmCallLogService

文件：

```text
src/main/java/com/example/aigateway/service/LlmCallLogService.java
```

```java
package com.example.aigateway.service;

import com.example.aigateway.dto.LlmCallLog;
import com.example.aigateway.dto.LlmCallType;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.springframework.stereotype.Service;

/**
 * 大模型调用日志服务。
 *
 * 当前使用内存 List 保存最近 100 条日志。
 * 生产环境应该替换为数据库、日志平台或 tracing 系统。
 */
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
        addLog(LlmCallLog.success(
                callType,
                model,
                latencyMs,
                promptTokens,
                completionTokens,
                totalTokens
        ));
    }

    public synchronized void recordFailure(
            LlmCallType callType,
            String model,
            long latencyMs,
            String errorMessage
    ) {
        addLog(LlmCallLog.failure(
                callType,
                model,
                latencyMs,
                errorMessage
        ));
    }

    public synchronized List<LlmCallLog> recentLogs() {
        List<LlmCallLog> copy = new ArrayList<>(logs);
        Collections.reverse(copy);
        return copy;
    }

    private void addLog(LlmCallLog log) {
        logs.add(log);

        while (logs.size() > MAX_SIZE) {
            logs.remove(0);
        }
    }
}
```
