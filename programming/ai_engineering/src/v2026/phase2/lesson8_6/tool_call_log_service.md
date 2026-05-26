# 修改 ToolCallLogService

把工具调用日志从内存 List 改成数据库持久化。

工具调用日志和模型调用日志需要共享 `traceId`，这样才能定位一次请求中：

```text
模型如何决策
调用了哪个工具
工具返回了什么
最终用户看到了什么
```

#### 代码

文件：

```text
src/main/java/com/example/aigateway/service/ToolCallLogService.java
```

替换为：

```java
package com.example.aigateway.service;

import com.example.aigateway.dto.ToolCallLog;
import com.example.aigateway.entity.ToolCallLogEntity;
import com.example.aigateway.repository.ToolCallLogRepository;
import com.example.aigateway.trace.TraceContext;
import java.time.Instant;
import java.util.List;
import org.springframework.stereotype.Service;

/**
 * 工具调用日志服务。
 *
 * 第 8.6 课升级：
 * - 从内存 List 改为数据库持久化
 * - 增加 requestId / traceId
 */
@Service
public class ToolCallLogService {

    private final ToolCallLogRepository repository;

    public ToolCallLogService(ToolCallLogRepository repository) {
        this.repository = repository;
    }

    public void record(ToolCallLog log) {
        ToolCallLogEntity entity = new ToolCallLogEntity();
        entity.setRequestId(TraceContext.getRequestId());
        entity.setTraceId(TraceContext.getTraceId());
        entity.setShouldCallTool(log.shouldCallTool());
        entity.setToolName(log.toolName());
        entity.setArgumentsJson(log.argumentsJson());
        entity.setToolResult(log.toolResult());
        entity.setSuccess(log.success());
        entity.setLatencyMs(log.latencyMs());
        entity.setErrorMessage(log.errorMessage());
        entity.setCreatedAt(Instant.now());

        repository.save(entity);
    }

    public List<ToolCallLogEntity> recentLogs() {
        return repository.findTop100ByOrderByCreatedAtDesc();
    }

    public List<ToolCallLogEntity> findByToolName(String toolName) {
        return repository.findTop100ByToolNameOrderByCreatedAtDesc(toolName);
    }

    public List<ToolCallLogEntity> findBySuccess(boolean success) {
        return repository.findTop100BySuccessOrderByCreatedAtDesc(success);
    }

    public List<ToolCallLogEntity> findByTraceId(String traceId) {
        return repository.findTop100ByTraceIdOrderByCreatedAtDesc(traceId);
    }
}
```

#### 代码说明

`ToolCallLog` 可以继续作为业务侧日志 DTO，`ToolCallLogEntity` 作为数据库实体。
