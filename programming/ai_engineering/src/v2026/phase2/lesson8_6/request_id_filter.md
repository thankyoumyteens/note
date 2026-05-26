# 新增 RequestIdFilter

为每个请求自动生成 `requestId` 和 `traceId`。

Filter 会在 Controller 之前执行。它适合做：

```text
requestId 生成
traceId 生成
日志上下文初始化
请求结束后的上下文清理
```

#### 代码

文件：

```text
src/main/java/com/example/aigateway/trace/RequestIdFilter.java
```

代码：

```java
package com.example.aigateway.trace;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.UUID;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

/**
 * 为每个 HTTP 请求生成 requestId / traceId。
 *
 * requestId：
 * - 当前服务内的一次请求 ID
 *
 * traceId：
 * - 用于跨服务链路追踪
 * - 当前阶段先和 requestId 使用同一个值
 */
@Component
public class RequestIdFilter extends OncePerRequestFilter {

    private static final String REQUEST_ID_HEADER = "X-Request-Id";
    private static final String TRACE_ID_HEADER = "X-Trace-Id";

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain
    ) throws ServletException, IOException {

        String requestId = getOrCreateHeader(request, REQUEST_ID_HEADER);
        String traceId = getOrCreateHeader(request, TRACE_ID_HEADER);

        try {
            TraceContext.set(requestId, traceId);

            response.setHeader(REQUEST_ID_HEADER, requestId);
            response.setHeader(TRACE_ID_HEADER, traceId);

            filterChain.doFilter(request, response);

        } finally {
            TraceContext.clear();
        }
    }

    private String getOrCreateHeader(HttpServletRequest request, String headerName) {
        String value = request.getHeader(headerName);

        if (value == null || value.isBlank()) {
            return UUID.randomUUID().toString();
        }

        return value.strip();
    }
}
```

#### 代码说明

如果客户端传入：

```text
X-Request-Id
X-Trace-Id
```

就沿用客户端提供的值。

如果没有传，就服务端生成 UUID。

#### 常见错误

```text
1. 忘记 finally clear
2. 没把 requestId 写回 response header
3. 把 requestId 和 traceId 混为一谈；当前只是简化实现
```
