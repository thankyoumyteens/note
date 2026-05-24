# 新增 RateLimitStatusController

提供一个简单接口确认限流功能已启用。

这是调试接口，不是生产用户接口。生产环境需要加权限控制。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/controller/RateLimitStatusController.java
```

代码：

```java
package com.example.aigateway.controller;

import com.example.aigateway.config.RateLimitProperties;
import com.example.aigateway.dto.RateLimitStatus;
import org.springframework.web.bind.annotation.*;

/**
 * 限流状态查询接口。
 *
 * 当前用于本地调试。
 * 生产环境应该加权限控制。
 */
@RestController
@RequestMapping("/api/ai")
public class RateLimitStatusController {

    private final RateLimitProperties properties;

    public RateLimitStatusController(RateLimitProperties properties) {
        this.properties = properties;
    }

    @GetMapping("/rate-limit-status")
    public RateLimitStatus status() {
        return new RateLimitStatus(
                properties.isEnabled(),
                "redis-fixed-window",
                "Redis distributed rate limiter is configured for AI Gateway."
        );
    }
}
```

#### 代码说明

调用：

```http
GET /api/ai/rate-limit-status
```

可以看到当前限流是否启用。
