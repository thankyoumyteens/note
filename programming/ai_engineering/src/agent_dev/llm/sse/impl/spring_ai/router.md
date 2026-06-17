# Provider Router

这个 Router 根据请求里的 `provider` 选择不同的 `ChatClient`。

```java
package com.example.ai.service;

import com.example.ai.dto.StreamChatRequest;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;

/**
 * Spring AI 多 provider 流式路由。
 * 统一返回 Flux<String>，Controller 再包装成 SSE。
 */
@Service
public class SpringAiStreamRouter {

    private final ChatClient openAiChatClient;
    private final ChatClient deepSeekChatClient;
    private final ChatClient claudeChatClient;

    public SpringAiStreamRouter(
            @Qualifier("openAiChatClient") ChatClient openAiChatClient,
            @Qualifier("deepSeekChatClient") ChatClient deepSeekChatClient,
            @Qualifier("claudeChatClient") ChatClient claudeChatClient
    ) {
        this.openAiChatClient = openAiChatClient;
        this.deepSeekChatClient = deepSeekChatClient;
        this.claudeChatClient = claudeChatClient;
    }

    public Flux<String> stream(StreamChatRequest request) {
        ChatClient chatClient = selectChatClient(request.provider());

        ChatClient.ChatClientRequestSpec prompt = chatClient.prompt();

        if (request.system() != null && !request.system().isBlank()) {
            prompt = prompt.system(request.system());
        }

        return prompt
                .user(request.message())
                .stream()
                .content();
    }

    private ChatClient selectChatClient(String provider) {
        return switch (provider) {
            case "openai" -> openAiChatClient;
            case "deepseek" -> deepSeekChatClient;
            case "claude" -> claudeChatClient;
            default -> throw new IllegalArgumentException(
                    "Unsupported provider: " + provider
            );
        };
    }
}
```

核心代码是：

```java
return prompt
        .user(request.message())
        .stream()
        .content();
```

它返回：

```java
Flux<String>
```

Spring AI 的价值就在这里：你不再需要自己写：

```java
OpenAI: choices[0].delta.content
Claude: content_block_delta.data.delta.text
```

这些 provider 原始流解析逻辑。
