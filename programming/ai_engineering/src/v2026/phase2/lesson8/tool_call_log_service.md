# 新增 ToolCallLogService

文件：

```text
src/main/java/com/example/aigateway/service/ToolCallLogService.java
```

```java
package com.example.aigateway.service;

import com.example.aigateway.dto.ToolCallLog;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.springframework.stereotype.Service;

/**
 * 工具调用日志服务。
 *
 * 当前内存保存最近 100 条。
 * 用于第 8 课 Tool Decision Trace。
 */
@Service
public class ToolCallLogService {

    private static final int MAX_SIZE = 100;

    private final List<ToolCallLog> logs = new ArrayList<>();

    public synchronized void record(ToolCallLog log) {
        logs.add(log);

        while (logs.size() > MAX_SIZE) {
            logs.remove(0);
        }
    }

    public synchronized List<ToolCallLog> recentLogs() {
        List<ToolCallLog> copy = new ArrayList<>(logs);
        Collections.reverse(copy);
        return copy;
    }
}
```
