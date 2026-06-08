# 新增工具 DTO

给工具建立统一数据结构。

一个工具至少需要这些信息：

```text
name：工具名
description：工具做什么
parameters：需要哪些参数
requiredRoles：哪些角色可以调用
dangerous：是否高风险
```

第 17 课先做简化版，不做完整 JSON Schema。

### 代码

目录：

```text
src/main/java/com/example/aigateway/tool/dto/
```

`ToolParameterDefinition.java`

```java
package com.example.aigateway.tool.dto;

/**
 * 工具参数定义。
 *
 * 第 17 课先做简化版参数 schema。
 */
public record ToolParameterDefinition(
        String name,
        String type,
        boolean required,
        String description
) {
}
```

`ToolDefinition.java`

```java
package com.example.aigateway.tool.dto;

import java.util.List;

/**
 * 工具定义。
 *
 * description 会影响模型是否选对工具。
 * requiredRoles 用于工具权限检查。
 */
public record ToolDefinition(
        String name,
        String description,
        List<ToolParameterDefinition> parameters,
        List<String> requiredRoles,
        boolean dangerous
) {
}
```

`ToolRequest.java`

```java
package com.example.aigateway.tool.dto;

import java.util.Map;
import java.util.UUID;

/**
 * 工具调用请求。
 */
public record ToolRequest(
        UUID workflowId,
        String toolName,
        Map<String, Object> arguments
) {
}
```

`ToolResult.java`

```java
package com.example.aigateway.tool.dto;

import java.util.Map;

/**
 * 工具调用结果。
 *
 * success=false 时，errorCode / errorMessage 必须有意义。
 */
public record ToolResult(
        boolean success,
        String toolName,
        Map<String, Object> data,
        String errorCode,
        String errorMessage
) {
    public static ToolResult success(String toolName, Map<String, Object> data) {
        return new ToolResult(
                true,
                toolName,
                data,
                null,
                null
        );
    }

    public static ToolResult failure(
            String toolName,
            String errorCode,
            String errorMessage
    ) {
        return new ToolResult(
                false,
                toolName,
                Map.of(),
                errorCode,
                errorMessage
        );
    }
}
```

### 代码说明

`ToolResult` 不应该只返回一段自然语言。它要有结构化错误：

```text
success
errorCode
errorMessage
data
```

这样 Agent 才能判断：

```text
工具成功了？
失败是参数错？
权限不足？
业务不存在？
系统异常？
```
