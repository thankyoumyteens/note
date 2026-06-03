# 新增 CurrentUserContextFilter

从请求头中读取 tenantId、userId、roles，并写入 `CurrentUserContextHolder`。

Filter 在 Controller 之前执行，很适合做请求级上下文初始化。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/security/CurrentUserContextFilter.java
```

```java
package com.example.aigateway.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

/**
 * 当前用户上下文过滤器。
 *
 * 第 14 课先用请求头模拟用户身份。
 *
 * 示例：
 * X-Tenant-Id: tenant-a
 * X-User-Id: user-001
 * X-Roles: finance,employee
 */
@Component
public class CurrentUserContextFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain
    ) throws ServletException, IOException {
        try {
            String tenantId = readRequiredHeader(request, "X-Tenant-Id");
            String userId = readRequiredHeader(request, "X-User-Id");
            List<String> roles = parseRoles(request.getHeader("X-Roles"));

            CurrentUserContextHolder.set(
                    new CurrentUserContext(
                            tenantId,
                            userId,
                            roles
                    )
            );

            filterChain.doFilter(request, response);
        } finally {
            CurrentUserContextHolder.clear();
        }
    }

    private String readRequiredHeader(HttpServletRequest request, String name) {
        String value = request.getHeader(name);

        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("Missing required header: " + name);
        }

        return value.strip();
    }

    private List<String> parseRoles(String rawRoles) {
        if (rawRoles == null || rawRoles.isBlank()) {
            return List.of();
        }

        return Arrays.stream(rawRoles.split(","))
                .map(String::strip)
                .filter(role -> !role.isBlank())
                .toList();
    }
}
```

#### 代码说明

现在所有请求都需要带这两个 header：

```http
X-Tenant-Id
X-User-Id
```

如果你不想影响 `/api/health`，可以在 Filter 里跳过健康检查路径：

```java
@Override
protected boolean shouldNotFilter(HttpServletRequest request) {
    return request.getRequestURI().equals("/api/health");
}
```
