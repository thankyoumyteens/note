# 新增 CurrentUserContext

在没有完整登录系统的情况下，先用一个上下文对象表示当前请求用户。

生产系统中，当前用户通常来自：

```text
JWT
Session
OAuth2
Spring Security Authentication
API Gateway header
```

本课为了不跳到认证系统，先用请求头模拟。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/security/CurrentUserContext.java
```

```java
package com.example.aigateway.security;

import java.util.List;

/**
 * 当前请求用户上下文。
 *
 * 第 14 课先通过请求头模拟：
 * - X-Tenant-Id
 * - X-User-Id
 * - X-Roles
 *
 * 后续接入 Spring Security 后，可以从 Authentication 中构造该对象。
 */
public record CurrentUserContext(
        String tenantId,
        String userId,
        List<String> roles
) {
    public boolean hasRole(String role) {
        return roles != null && roles.contains(role);
    }
}
```
