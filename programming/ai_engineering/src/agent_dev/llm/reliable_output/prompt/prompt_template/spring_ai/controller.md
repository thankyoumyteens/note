# Controller 使用方式

```java
package com.example.llm.controller;

import com.example.llm.dto.UnifiedChatResponse;
import com.example.llm.service.IntentClassificationService;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.UUID;

@RestController
@RequestMapping("/api/intents")
public class IntentClassificationController {

    // 执行 Spring AI Prompt 渲染和统一模型调用。
    private final IntentClassificationService service;

    public IntentClassificationController(IntentClassificationService service) {
        this.service = service;
    }

    @PostMapping("/classify")
    public UnifiedChatResponse classify(@RequestBody IntentClassificationRequest request) {
        String requestId = UUID.randomUUID().toString();
        String traceId = requestId;

        return service.classify(request.userInput(), requestId, traceId);
    }

    public record IntentClassificationRequest(
            String userInput // 需要识别意图的原始用户输入。
    ) {

        public IntentClassificationRequest {
            if (userInput == null || userInput.isBlank()) {
                throw new IllegalArgumentException("userInput must not be blank");
            }
        }
    }
}
```

## 测试接口

```sh
curl -sS -X POST "http://localhost:8080/api/intents/classify" \
  -H "Content-Type: application/json" \
  -d '{
    "userInput": "帮我查询订单 20260717001"
  }' | jq
```
