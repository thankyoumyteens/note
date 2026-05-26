# 新增 TraceContext

保存当前请求的 `requestId` 和 `traceId`，让后续模型调用日志、工具调用日志可以关联到同一次请求。

`ThreadLocal` 可以保存当前线程上下文。

在普通 Spring MVC 请求里，一个请求通常由一个线程处理，所以可以用 `ThreadLocal` 暂存 requestId / traceId。

注意：复杂异步、Reactive、跨线程场景下，`ThreadLocal` 可能失效。完整方案后续应使用 OpenTelemetry / Reactor Context。本课先做 Servlet 请求级基础版本。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/trace/TraceContext.java
```

代码：

```java
package com.example.aigateway.trace;

/**
 * 请求追踪上下文。
 *
 * 当前用 ThreadLocal 保存 requestId / traceId。
 *
 * 注意：
 * - 适合当前 Spring MVC 同线程请求链路
 * - 复杂异步 / Reactor 场景后续应升级为 OpenTelemetry 或 Reactor Context
 */
public final class TraceContext {

    private static final ThreadLocal<String> REQUEST_ID = new ThreadLocal<>();
    private static final ThreadLocal<String> TRACE_ID = new ThreadLocal<>();

    private TraceContext() {
    }

    public static void set(String requestId, String traceId) {
        REQUEST_ID.set(requestId);
        TRACE_ID.set(traceId);
    }

    public static String getRequestId() {
        return REQUEST_ID.get();
    }

    public static String getTraceId() {
        return TRACE_ID.get();
    }

    public static void clear() {
        REQUEST_ID.remove();
        TRACE_ID.remove();
    }
}
```

#### 代码说明

每个 HTTP 请求进来时设置：

```text
requestId
traceId
```

请求结束时必须清理，避免线程复用导致串数据。

#### 常见错误

```text
1. 设置了 ThreadLocal 但没有 clear
2. 在异步线程里直接读取 TraceContext，结果为空
3. 把 ThreadLocal 当成完整 tracing 系统
```
