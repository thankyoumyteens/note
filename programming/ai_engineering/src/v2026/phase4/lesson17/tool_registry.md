# 新增 ToolRegistry

集中管理所有工具。

Tool Registry 的作用是：

```text
注册工具
查找工具
列出工具定义给 Planner
统一执行工具
```

这也是后续 MCP 接入前的重要铺垫。

### 代码

文件：

```text
src/main/java/com/example/aigateway/tool/service/ToolRegistry.java
```

```java
package com.example.aigateway.tool.service;

import com.example.aigateway.tool.dto.ToolDefinition;
import com.example.aigateway.tool.dto.ToolRequest;
import com.example.aigateway.tool.dto.ToolResult;
import com.example.aigateway.tool.executor.ToolExecutor;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

/**
 * 工具注册表。
 *
 * Spring 会把所有 ToolExecutor 注入进来。
 */
@Service
public class ToolRegistry {

    private final Map<String, ToolExecutor> executors;

    public ToolRegistry(List<ToolExecutor> executors) {
        this.executors = executors.stream()
                .collect(Collectors.toMap(
                        executor -> executor.definition().name(),
                        executor -> executor
                ));
    }

    public List<ToolDefinition> listTools() {
        return executors.values().stream()
                .map(ToolExecutor::definition)
                .toList();
    }

    public ToolResult execute(ToolRequest request) {
        ToolExecutor executor = executors.get(request.toolName());

        if (executor == null) {
            return ToolResult.failure(
                    request.toolName(),
                    "TOOL_NOT_FOUND",
                    "tool not found: " + request.toolName()
            );
        }

        return executor.execute(request);
    }

    public ToolDefinition getRequiredDefinition(String toolName) {
        ToolExecutor executor = executors.get(toolName);

        if (executor == null) {
            throw new IllegalArgumentException("tool not found: " + toolName);
        }

        return executor.definition();
    }
}
```
