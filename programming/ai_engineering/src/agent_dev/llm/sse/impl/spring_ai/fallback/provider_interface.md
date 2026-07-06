# 统一 ProviderClient 接口

```java id="2jvz5w"
package com.example.llm.provider;

import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatStreamEvent;
import reactor.core.publisher.Flux;

/**
 * 所有 Spring AI stream provider 的统一接口。
 */
public interface LlmStreamProviderClient {

    String provider();

    Flux<UnifiedChatStreamEvent> stream(UnifiedChatRequest request);
}
```
