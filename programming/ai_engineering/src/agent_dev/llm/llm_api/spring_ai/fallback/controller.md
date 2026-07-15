# Controller 使用方式

```java
package com.example.llm.controller;

import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatResponse;
import com.example.llm.router.ProviderFallbackRouter;
import org.springframework.web.bind.annotation.*;

/**
 * 普通非 SSE 聊天接口。
 */
@RestController
@RequestMapping("/api/llm")
public class LlmController {

    private final ProviderFallbackRouter router;

    public LlmController(ProviderFallbackRouter router) {
        this.router = router;
    }

    @PostMapping("/chat")
    public UnifiedChatResponse chat(@RequestBody UnifiedChatRequest request) {
        return router.chat(request);
    }
}
```

## 测试请求

```bash
curl -sS -X POST "http://localhost:8080/api/llm/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "system": "你是一个严谨的 Java 后端助手。",
    "messages": [
      {
        "role": "USER",
        "content": "用一句话解释什么是 RAG。"
      }
    ],
    "options": {
      "temperature": 0.2,
      "maxTokens": 300,
      "topP": null
    },
    "metadata": {}
  }' | jq
```
