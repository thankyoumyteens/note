# Controller 测试接口

```java
package com.example.ai;

import org.springframework.web.bind.annotation.*;

/**
 * 多 provider 聊天接口。
 * 请求里传 provider，后端路由到对应模型。
 */
@RestController
@RequestMapping("/api/ai")
public class AiChatController {

    private final LlmRouterService llmRouterService;

    public AiChatController(LlmRouterService llmRouterService) {
        this.llmRouterService = llmRouterService;
    }

    @PostMapping("/chat")
    public ChatResponse chat(@RequestBody ChatRequest request) {
        String content = llmRouterService.chat(request.provider(), request.message());
        return new ChatResponse(request.provider(), content);
    }

    public record ChatRequest(
            LlmProvider provider,
            String message
    ) {
    }

    public record ChatResponse(
            LlmProvider provider,
            String content
    ) {
    }
}
```

## 调用方式

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "QWEN",
    "message": "用一句话解释什么是 RAG"
  }'
```

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "OPENAI",
    "message": "用一句话解释什么是 RAG"
  }'
```

```bash
curl -X POST http://localhost:8080/api/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "CLAUDE",
    "message": "用一句话解释什么是 RAG"
  }'
```
