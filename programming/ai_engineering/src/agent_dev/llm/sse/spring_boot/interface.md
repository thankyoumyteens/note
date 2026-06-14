# 统一 Streaming Client 接口

```java
package com.example.ai.client;

import com.example.ai.config.AiProviderProperties;
import com.example.ai.dto.StreamChatRequest;
import reactor.core.publisher.Flux;

/**
 * Provider streaming client 统一接口。
 */
public interface ProviderStreamClient {

    boolean supports(AiProviderProperties.ProviderType type);

    Flux<String> stream(AiProviderProperties.ProviderConfig config,
                        StreamChatRequest request);
}
```

这里返回 `Flux<String>`，只返回文本增量，不把 provider 原始 SSE 暴露到 Controller。
