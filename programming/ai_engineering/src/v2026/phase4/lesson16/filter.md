# Filter 只拦截需要用户上下文的接口

第 14 课时我们用请求头模拟用户身份，主要是为了保护 RAG 权限隔离。现在进入第 16 课，Agent 接口暂时还没有接入真实用户权限，所以可以让 Filter 只拦截 `/api/rag/**`，先不拦截 `/api/agent/**`。

修改 `CurrentUserContextFilter`，加上：

```java
@Override
protected boolean shouldNotFilter(HttpServletRequest request) {
    String path = request.getRequestURI();

    return !path.startsWith("/api/rag/");
}
```

这样：

```text
/api/rag/**      需要 X-Tenant-Id / X-User-Id
/api/agent/**    暂时不需要
/api/health      不需要
/api/ai/**       不需要
```
