# Controller 使用方式

Controller 不处理 timeout、retry、fallback。

```java
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/llm")
public class LlmController {

    private final ProviderFallbackRouter router;

    public LlmController(ProviderFallbackRouter router) {
        this.router = router;
    }

    @PostMapping("/chat")
    public UnifiedChatResponse chat(@RequestBody UnifiedChatRequest request) {
        return router.chat(request)
                .block();
    }
}
```

## 测试接口

```sh
curl -s -X POST "http://localhost:8080/api/llm/chat" \
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
