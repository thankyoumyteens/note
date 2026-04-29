# 第一个接口设计

## ChatRequest

```java
package com.example.aigateway.dto;

public record ChatRequest(
        String message
) {
}
```

## ChatResponse

```java
package com.example.aigateway.dto;

public record ChatResponse(
        String answer
) {
}
```

## LlmClient

```java
package com.example.aigateway.client;

public interface LlmClient {

    String chat(String message);
}
```

## AiChatService

```java
package com.example.aigateway.service;

import com.example.aigateway.client.LlmClient;
import org.springframework.stereotype.Service;

@Service
public class AiChatService {

    private final LlmClient llmClient;

    public AiChatService(LlmClient llmClient) {
        this.llmClient = llmClient;
    }

    public String chat(String message) {
        if (message == null || message.isBlank()) {
            throw new IllegalArgumentException("message cannot be empty");
        }

        return llmClient.chat(message);
    }
}
```

## AiChatController

```java
package com.example.aigateway.controller;

import com.example.aigateway.dto.ChatRequest;
import com.example.aigateway.dto.ChatResponse;
import com.example.aigateway.service.AiChatService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/ai")
public class AiChatController {

    private final AiChatService aiChatService;

    public AiChatController(AiChatService aiChatService) {
        this.aiChatService = aiChatService;
    }

    @PostMapping("/chat")
    public ChatResponse chat(@RequestBody ChatRequest request) {
        String answer = aiChatService.chat(request.message());
        return new ChatResponse(answer);
    }
}
```
