# 新增 Controller

文件：

```text
src/main/java/com/example/aigateway/controller/OrderAssistantController.java
```

代码：

```java
package com.example.aigateway.controller;

import com.example.aigateway.dto.OrderAssistantRequest;
import com.example.aigateway.dto.OrderAssistantResponse;
import com.example.aigateway.service.OrderAssistantService;
import org.springframework.web.bind.annotation.*;

/**
 * 订单助手接口。
 *
 * 该接口演示 Function Calling / Tool Calling 的基础流程：
 * 用户自然语言请求 -> 模型生成工具调用决策 -> Java 后端执行工具。
 */
@RestController
@RequestMapping("/api/ai")
public class OrderAssistantController {

    private final OrderAssistantService orderAssistantService;

    public OrderAssistantController(OrderAssistantService orderAssistantService) {
        this.orderAssistantService = orderAssistantService;
    }

    /**
     * 订单助手入口。
     */
    @PostMapping("/order-assistant")
    public OrderAssistantResponse handle(@RequestBody OrderAssistantRequest request) {
        String answer = orderAssistantService.handle(request.message());
        return new OrderAssistantResponse(answer);
    }
}
```
