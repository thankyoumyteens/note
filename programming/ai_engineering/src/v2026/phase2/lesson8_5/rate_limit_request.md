# 新增 RateLimitRequest

封装一次限流判断需要的信息。

限流不是只问“能不能调用”，还要问：

```text
谁在调用？
调用什么模型？
调用什么类型？
调用哪个接口？
属于哪个租户？
```

当前项目还没有用户和租户系统，所以先用：

```text
callType
model
```

#### 代码

文件：

```text
src/main/java/com/example/aigateway/dto/RateLimitRequest.java
```

代码：

```java
package com.example.aigateway.dto;

/**
 * 限流请求上下文。
 *
 * 当前阶段主要使用：
 * - callType：模型调用类型
 * - model：模型名称
 *
 * 后续有登录、租户、API Key 后，可以继续扩展：
 * - userId
 * - tenantId
 * - apiKey
 * - ip
 */
public record RateLimitRequest(
        LlmCallType callType,
        String model,
        String endpoint,
        String userId,
        String tenantId,
        String ip
) {
    /**
     * 当前 LLM 调用场景的快捷构造方法。
     */
    public static RateLimitRequest forLlmCall(
            LlmCallType callType,
            String model
    ) {
        return new RateLimitRequest(
                callType,
                model,
                null,
                "anonymous",
                "default",
                null
        );
    }
}
```

`forLlmCall` 是为了让模型调用处写起来更简单：

```java
RateLimitRequest.forLlmCall(callType, properties.getModel())
```
