# 新增 Controller

新建：

```text
controller/OrderAssistantController.java
```

```java
package com.example.aigateway.controller;

import com.example.aigateway.dto.OrderAssistantRequest;
import com.example.aigateway.dto.OrderAssistantResponse;
import com.example.aigateway.service.OrderAssistantService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/ai")
public class OrderAssistantController {

    private final OrderAssistantService orderAssistantService;

    public OrderAssistantController(OrderAssistantService orderAssistantService) {
        this.orderAssistantService = orderAssistantService;
    }

    @PostMapping("/order-assistant")
    public OrderAssistantResponse handle(@RequestBody OrderAssistantRequest request) {
        String answer = orderAssistantService.handle(request.message());
        return new OrderAssistantResponse(answer);
    }
}
```
