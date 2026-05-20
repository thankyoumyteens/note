# 修改 Controller

文件：

```text
src/main/java/com/example/aigateway/controller/AiChatController.java
```

改成：

```java
package com.example.aigateway.controller;

import com.example.aigateway.dto.ChatRequest;
import com.example.aigateway.dto.ChatResponse;
import com.example.aigateway.service.AiChatService;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

/**
 * AI 聊天接口。
 */
@RestController
@RequestMapping("/api/ai")
public class AiChatController {

    private final AiChatService aiChatService;

    public AiChatController(AiChatService aiChatService) {
        this.aiChatService = aiChatService;
    }

    /**
     * 普通聊天接口。
     *
     * 返回 JSON：
     * {
     *   "answer": "完整回答"
     * }
     */
    @PostMapping("/chat")
    public ChatResponse chat(@RequestBody ChatRequest request) {
        String answer = aiChatService.chat(request.message());
        return new ChatResponse(answer);
    }

    /**
     * 流式聊天接口。
     *
     * produces = text/event-stream 表示返回 SSE。
     * 客户端会持续收到 data: xxx 形式的事件。
     */
    @PostMapping(value = "/chat/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> streamChat(@RequestBody ChatRequest request) {
        return aiChatService.streamChat(request.message());
    }
}
```

重点是这一行：

```java
@PostMapping(value = "/chat/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
```

它告诉 Spring：这个接口返回 SSE 流，而不是普通 JSON。如果没有这个声明，客户端可能不会按 SSE 流来处理响应。
