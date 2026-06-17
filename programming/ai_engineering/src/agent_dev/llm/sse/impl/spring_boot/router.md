# Router：根据 provider 切换

```java
package com.example.ai.service;

import com.example.ai.client.ProviderStreamClient;
import com.example.ai.config.AiProviderProperties;
import com.example.ai.dto.StreamChatRequest;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;

import java.util.List;

/**
 * 多 provider streaming 路由服务。
 * 根据 request.provider 选择不同协议的 streaming client。
 */
@Service
public class LlmStreamRouter {

    private final AiProviderProperties properties;
    private final List<ProviderStreamClient> clients;

    public LlmStreamRouter(AiProviderProperties properties,
                           List<ProviderStreamClient> clients) {
        this.properties = properties;
        this.clients = clients;
    }

    public Flux<String> stream(StreamChatRequest request) {
        AiProviderProperties.ProviderConfig config =
                properties.getRequiredProvider(request.provider());

        ProviderStreamClient client = clients.stream()
                .filter(candidate -> candidate.supports(config.type()))
                .findFirst()
                .orElseThrow(() -> new IllegalStateException(
                        "No stream client for provider type: " + config.type()
                ));

        return client.stream(config, request);
    }
}
```

这个设计的好处是：

- provider 名称可以无限扩展：qwen / deepseek / openai / claude / qwen-messages
- 协议类型只需要几类：
  - openai-chat-completions
  - anthropic-messages
  - responses-api 后续可以再加
