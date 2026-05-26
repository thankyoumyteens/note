# 修改 LlmCallLogService

把模型调用日志从内存 List 改成数据库持久化。

Service 层负责把调用参数转换成 Entity，然后交给 Repository 保存。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/service/LlmCallLogService.java
```

替换为：

```java
package com.example.aigateway.service;

import com.example.aigateway.dto.LlmCallStats;
import com.example.aigateway.dto.LlmCallType;
import com.example.aigateway.entity.LlmCallLogEntity;
import com.example.aigateway.repository.LlmCallLogRepository;
import com.example.aigateway.trace.TraceContext;
import java.time.Instant;
import java.util.List;
import org.springframework.stereotype.Service;

/**
 * 模型调用日志服务。
 *
 * 第 8.6 课升级：
 * - 从内存 List 改为数据库持久化
 * - 增加 requestId / traceId
 * - 支持基础统计
 */
@Service
public class LlmCallLogService {

    private final LlmCallLogRepository repository;

    public LlmCallLogService(LlmCallLogRepository repository) {
        this.repository = repository;
    }

    public void recordSuccess(
            LlmCallType callType,
            String model,
            long latencyMs,
            Integer promptTokens,
            Integer completionTokens,
            Integer totalTokens
    ) {
        LlmCallLogEntity entity = new LlmCallLogEntity();
        entity.setRequestId(TraceContext.getRequestId());
        entity.setTraceId(TraceContext.getTraceId());
        entity.setCallType(callType);
        entity.setModel(model);
        entity.setSuccess(true);
        entity.setLatencyMs(latencyMs);
        entity.setPromptTokens(promptTokens);
        entity.setCompletionTokens(completionTokens);
        entity.setTotalTokens(totalTokens);
        entity.setErrorMessage(null);
        entity.setCreatedAt(Instant.now());

        repository.save(entity);
    }

    public void recordFailure(
            LlmCallType callType,
            String model,
            long latencyMs,
            String errorMessage
    ) {
        LlmCallLogEntity entity = new LlmCallLogEntity();
        entity.setRequestId(TraceContext.getRequestId());
        entity.setTraceId(TraceContext.getTraceId());
        entity.setCallType(callType);
        entity.setModel(model);
        entity.setSuccess(false);
        entity.setLatencyMs(latencyMs);
        entity.setPromptTokens(null);
        entity.setCompletionTokens(null);
        entity.setTotalTokens(null);
        entity.setErrorMessage(errorMessage);
        entity.setCreatedAt(Instant.now());

        repository.save(entity);
    }

    public List<LlmCallLogEntity> recentLogs() {
        return repository.findTop100ByOrderByCreatedAtDesc();
    }

    public List<LlmCallLogEntity> findByCallType(LlmCallType callType) {
        return repository.findTop100ByCallTypeOrderByCreatedAtDesc(callType);
    }

    public List<LlmCallLogEntity> findByModel(String model) {
        return repository.findTop100ByModelOrderByCreatedAtDesc(model);
    }

    public List<LlmCallLogEntity> findBySuccess(boolean success) {
        return repository.findTop100BySuccessOrderByCreatedAtDesc(success);
    }

    public List<LlmCallLogEntity> findByTraceId(String traceId) {
        return repository.findTop100ByTraceIdOrderByCreatedAtDesc(traceId);
    }

    public LlmCallStats stats() {
        List<LlmCallLogEntity> logs = repository.findTop100ByOrderByCreatedAtDesc();

        long total = logs.size();
        long success = logs.stream().filter(LlmCallLogEntity::isSuccess).count();
        long failure = total - success;

        double avgLatencyMs = logs.stream()
                .mapToLong(LlmCallLogEntity::getLatencyMs)
                .average()
                .orElse(0);

        long totalTokens = logs.stream()
                .map(LlmCallLogEntity::getTotalTokens)
                .filter(value -> value != null)
                .mapToLong(Integer::longValue)
                .sum();

        return new LlmCallStats(
                total,
                success,
                failure,
                avgLatencyMs,
                totalTokens
        );
    }
}
```

#### 代码说明

这里的 `stats()` 先只统计最近 100 条。

生产环境应该用数据库聚合查询，而不是把日志查出来后在内存 stream 统计。本课先保持简单。
