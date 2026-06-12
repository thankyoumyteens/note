# Controller 测试接口

```java
package com.example.llm;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/llm")
public class LlmController {

    private final LlmClient llmClient;

    public LlmController(LlmClient llmClient) {
        this.llmClient = llmClient;
    }

    @PostMapping("/chat")
    public LlmChatResponse chat(@RequestBody LlmChatRequest request) {
        String answer = llmClient.chat(request.provider(), request.message());
        return new LlmChatResponse(request.provider(), answer);
    }

    public record LlmChatRequest(
            String provider,
            String message
    ) {
    }

    public record LlmChatResponse(
            String provider,
            String content
    ) {
    }
}
```

## 调用方式

```bash
curl -X POST http://localhost:8080/api/llm/chat \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "openai",
    "message": "用一句话解释什么是 RAG"
  }'
```

换 Qwen：

```json
{
  "provider": "qwen",
  "message": "用一句话解释什么是 RAG"
}
```
