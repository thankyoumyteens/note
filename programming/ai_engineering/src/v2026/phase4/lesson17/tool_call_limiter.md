# 新增 ToolCallLimiter

限制单个 workflow 的工具调用次数。

第 16 课限制 `stepCount`，第 17 课限制 `toolCallCount`。

建议在 `AgentTicket` 中新增字段：

```java
private int toolCallCount;
```

并增加：

```java
public void incrementToolCallCount() {
    toolCallCount++;
    updatedAt = Instant.now();
}
```

### 代码

文件：

```text
src/main/java/com/example/aigateway/tool/service/ToolCallLimiter.java
```

```java
package com.example.aigateway.tool.service;

import com.example.aigateway.agent.model.AgentTicket;
import com.example.aigateway.tool.config.ToolProperties;
import org.springframework.stereotype.Service;

/**
 * 工具调用次数限制。
 */
@Service
public class ToolCallLimiter {

    private final ToolProperties properties;

    public ToolCallLimiter(ToolProperties properties) {
        this.properties = properties;
    }

    public boolean allow(AgentTicket ticket) {
        return ticket.getToolCallCount() < properties.getMaxToolCallsPerWorkflow();
    }
}
```

建议：**只要尝试调用工具，无论成功失败都计数。**
