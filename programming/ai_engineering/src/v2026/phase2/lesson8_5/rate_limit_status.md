# 新增 RateLimitStatus

定义限流状态接口的响应 DTO。

调试接口不要直接返回配置类本身，最好返回一个稳定的 DTO。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/dto/RateLimitStatus.java
```

代码：

```java
package com.example.aigateway.dto;

/**
 * 限流状态 DTO。
 *
 * 当前用于调试接口。
 */
public record RateLimitStatus(
        boolean enabled,
        String mode,
        String description
) {
}
```

#### 代码说明

字段含义：

```text
enabled：是否启用限流
mode：当前限流模式
description：说明
```
