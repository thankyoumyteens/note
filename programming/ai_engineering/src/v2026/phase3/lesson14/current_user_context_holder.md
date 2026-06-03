# 新增 CurrentUserContextHolder

让 Service / Repository 能拿到当前用户信息。

`ThreadLocal` 可以保存当前请求线程上的用户上下文。

注意：这是课程阶段的简化实现。生产中更推荐接入 Spring Security，然后从 `SecurityContextHolder` 获取当前用户。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/security/CurrentUserContextHolder.java
```

```java
package com.example.aigateway.security;

/**
 * 当前用户上下文 Holder。
 *
 * 使用 ThreadLocal 保存当前请求用户。
 *
 * 注意：
 * - 每个请求结束后必须 clear
 * - 否则线程复用时可能发生用户信息串线
 */
public final class CurrentUserContextHolder {

    private static final ThreadLocal<CurrentUserContext> HOLDER = new ThreadLocal<>();

    private CurrentUserContextHolder() {
    }

    public static void set(CurrentUserContext context) {
        HOLDER.set(context);
    }

    public static CurrentUserContext getRequired() {
        CurrentUserContext context = HOLDER.get();

        if (context == null) {
            throw new IllegalStateException("Current user context is missing");
        }

        return context;
    }

    public static void clear() {
        HOLDER.remove();
    }
}
```
