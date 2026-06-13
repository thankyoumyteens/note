# 统一调用代码：ChatClient

不管底层是 OpenAI、Claude、Qwen 还是 DeepSeek，上层业务代码尽量都写成这样，这段代码不需要改，就可以通过配置切换 provider：

```java
package com.example.ai;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Service;

/**
 * 统一的 AI 聊天服务。
 * 业务层只依赖 ChatClient，不直接关心底层是哪家模型 API。
 */
@Service
public class AiChatService {

    private final ChatClient chatClient;

    public AiChatService(ChatClient.Builder chatClientBuilder) {
        this.chatClient = chatClientBuilder
                .defaultSystem("你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。")
                .build();
    }

    /**
     * 发送用户问题并返回模型文本回答。
     */
    public String chat(String message) {
        return chatClient.prompt()
                .user(message)
                .call()
                .content();
    }
}
```

## Controller

```java
package com.example.ai;

import org.springframework.web.bind.annotation.*;

/**
 * 对外暴露一个简单聊天接口。
 * 前端只调用自己的后端，不直接接触模型 API Key。
 */
@RestController
@RequestMapping("/api/ai")
public class AiChatController {

    private final AiChatService aiChatService;

    public AiChatController(AiChatService aiChatService) {
        this.aiChatService = aiChatService;
    }

    /**
     * 普通非流式聊天接口。
     */
    @PostMapping("/chat")
    public ChatResponse chat(@RequestBody ChatRequest request) {
        return new ChatResponse(aiChatService.chat(request.message()));
    }

    public record ChatRequest(String message) {
    }

    public record ChatResponse(String content) {
    }
}
```
