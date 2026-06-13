# 路由服务

```java
package com.example.ai;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

/**
 * 多 provider 路由服务。
 * 上层只关心 provider，不关心底层是 OpenAI-compatible 还是 Anthropic。
 */
@Service
public class LlmRouterService {

    private final ChatClient openAiChatClient;
    private final ChatClient qwenChatClient;
    private final ChatClient claudeChatClient;

    public LlmRouterService(
            @Qualifier("openAiChatClient") ChatClient openAiChatClient,
            @Qualifier("qwenChatClient") ChatClient qwenChatClient,
            @Qualifier("claudeChatClient") ChatClient claudeChatClient
    ) {
        this.openAiChatClient = openAiChatClient;
        this.qwenChatClient = qwenChatClient;
        this.claudeChatClient = claudeChatClient;
    }

    /**
     * 根据 provider 选择不同 ChatClient。
     */
    public String chat(LlmProvider provider, String message) {
        ChatClient client = switch (provider) {
            case OPENAI -> openAiChatClient;
            case QWEN -> qwenChatClient;
            case CLAUDE -> claudeChatClient;
        };

        return client.prompt()
                .user(message)
                .call()
                .content();
    }
}
```
