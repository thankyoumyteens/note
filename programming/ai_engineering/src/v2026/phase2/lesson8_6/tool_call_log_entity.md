# 新增 ToolCallLogEntity

把工具调用决策和执行结果保存到数据库。

Tool Decision Trace 用于回答：

```text
模型是否决定调用工具？
调用了哪个工具？
参数是什么？
工具执行成功了吗？
工具结果是什么？
```

这对后续白盒 eval 很重要。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/entity/ToolCallLogEntity.java
```

代码：

```java
package com.example.aigateway.entity;

import jakarta.persistence.*;
import java.time.Instant;

/**
 * 工具调用日志数据库实体。
 */
@Entity
@Table(name = "tool_call_logs")
public class ToolCallLogEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String requestId;

    private String traceId;

    private boolean shouldCallTool;

    private String toolName;

    @Column(length = 4000)
    private String argumentsJson;

    @Column(length = 4000)
    private String toolResult;

    private boolean success;

    private long latencyMs;

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

    public boolean isShouldCallTool() {
        return shouldCallTool;
    }

    public void setShouldCallTool(boolean shouldCallTool) {
        this.shouldCallTool = shouldCallTool;
    }

    public String getToolName() {
        return toolName;
    }

    public void setToolName(String toolName) {
        this.toolName = toolName;
    }

    public String getArgumentsJson() {
        return argumentsJson;
    }

    public void setArgumentsJson(String argumentsJson) {
        this.argumentsJson = argumentsJson;
    }

    public String getToolResult() {
        return toolResult;
    }

    public void setToolResult(String toolResult) {
        this.toolResult = toolResult;
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

`argumentsJson` 保存工具参数 JSON，例如：

```json
{ "orderId": "10086" }
```

这让 eval 可以判断模型是否提取了正确参数。
