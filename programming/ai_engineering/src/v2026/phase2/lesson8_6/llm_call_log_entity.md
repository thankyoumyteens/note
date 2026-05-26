# 新增 LlmCallLogEntity

把原来的 `LlmCallLog` record 转成可以保存到数据库的 Entity。

DTO 和 Entity 不完全一样：

```text
DTO：用于接口返回
Entity：用于数据库持久化
```

本课为了简单，可以让 Controller 返回 Entity，但生产中建议转换为 DTO。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/entity/LlmCallLogEntity.java
```

代码：

```java
package com.example.aigateway.entity;

import com.example.aigateway.dto.LlmCallType;
import jakarta.persistence.*;
import java.time.Instant;

/**
 * 模型调用日志数据库实体。
 */
@Entity
@Table(name = "llm_call_logs")
public class LlmCallLogEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * 当前 HTTP 请求 ID。
     */
    private String requestId;

    /**
     * 链路追踪 ID。
     */
    private String traceId;

    @Enumerated(EnumType.STRING)
    private LlmCallType callType;

    private String model;

    private boolean success;

    private long latencyMs;

    private Integer promptTokens;

    private Integer completionTokens;

    private Integer totalTokens;

    @Column(length = 2000)
    private String errorMessage;

    private Instant createdAt;

    public Long getId() {
        return id;
    }

    public String getRequestId() {
        return requestId;
    }

    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }

    public String getTraceId() {
        return traceId;
    }

    public void setTraceId(String traceId) {
        this.traceId = traceId;
    }

    public LlmCallType getCallType() {
        return callType;
    }

    public void setCallType(LlmCallType callType) {
        this.callType = callType;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public boolean isSuccess() {
        return success;
    }

    public void setSuccess(boolean success) {
        this.success = success;
    }

    public long getLatencyMs() {
        return latencyMs;
    }

    public void setLatencyMs(long latencyMs) {
        this.latencyMs = latencyMs;
    }

    public Integer getPromptTokens() {
        return promptTokens;
    }

    public void setPromptTokens(Integer promptTokens) {
        this.promptTokens = promptTokens;
    }

    public Integer getCompletionTokens() {
        return completionTokens;
    }

    public void setCompletionTokens(Integer completionTokens) {
        this.completionTokens = completionTokens;
    }

    public Integer getTotalTokens() {
        return totalTokens;
    }

    public void setTotalTokens(Integer totalTokens) {
        this.totalTokens = totalTokens;
    }

    public String getErrorMessage() {
        return errorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.errorMessage = errorMessage;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Instant createdAt) {
        this.createdAt = createdAt;
    }
}
```

#### 代码说明

重点字段：

```text
requestId：定位一次请求
traceId：后续跨服务链路追踪
callType：区分模型调用类型
latencyMs：性能分析
totalTokens：成本统计
success：成功率统计
```
