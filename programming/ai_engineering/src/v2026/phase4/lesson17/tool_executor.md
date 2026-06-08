# 新增 ToolExecutor 接口

统一所有工具执行器的接口。

不要让 Agent 直接调用具体工具类。

应该是：

```text
AgentStepExecutor
  -> ToolRegistry
  -> ToolExecutor
```

这样后续增加工具不会改 Agent 核心流程。

### 代码

文件：

```text
src/main/java/com/example/aigateway/tool/executor/ToolExecutor.java
```

```java
package com.example.aigateway.tool.executor;

import com.example.aigateway.tool.dto.ToolDefinition;
import com.example.aigateway.tool.dto.ToolRequest;
import com.example.aigateway.tool.dto.ToolResult;

/**
 * 工具执行器接口。
 *
 * 每个工具需要提供：
 * - definition：工具描述和参数定义
 * - execute：工具执行逻辑
 */
public interface ToolExecutor {

    ToolDefinition definition();

    ToolResult execute(ToolRequest request);
}
```
