# 新增 ToolPermissionService

执行工具前检查当前用户角色是否允许调用该工具。

工具调用权限和 RAG 文档权限不是一回事。

RAG 权限控制的是：

```text
用户能不能检索某些文档
```

工具权限控制的是：

```text
用户能不能执行某个动作或查询某类业务数据
```

### 代码

文件：

```text
src/main/java/com/example/aigateway/tool/service/ToolPermissionService.java
```

```java
package com.example.aigateway.tool.service;

import com.example.aigateway.security.CurrentUserContext;
import com.example.aigateway.security.CurrentUserContextHolder;
import com.example.aigateway.tool.dto.ToolDefinition;
import java.util.List;
import org.springframework.stereotype.Service;

/**
 * 工具权限检查。
 */
@Service
public class ToolPermissionService {

    public boolean canCall(ToolDefinition definition) {
        CurrentUserContext currentUser = CurrentUserContextHolder.getRequired();

        List<String> requiredRoles = definition.requiredRoles();

        if (requiredRoles == null || requiredRoles.isEmpty()) {
            return true;
        }

        for (String role : currentUser.roles()) {
            if (requiredRoles.contains(role)) {
                return true;
            }
        }

        return false;
    }
}
```

### 注意

之前把 `CurrentUserContextFilter` 改成只拦截 `/api/rag/**`，现在第 17 课需要让 Agent 也能拿到用户上下文。

可以改成：

```java
@Override
protected boolean shouldNotFilter(HttpServletRequest request) {
    String path = request.getRequestURI();

    return !(path.startsWith("/api/rag/") || path.startsWith("/api/agent/"));
}
```

这样：

```text
/api/rag/**    需要用户上下文
/api/agent/**  需要用户上下文
/api/ai/**     暂时不需要
/api/health    不需要
```
