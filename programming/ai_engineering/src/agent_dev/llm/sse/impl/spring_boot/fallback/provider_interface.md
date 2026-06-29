# 统一 ProviderClient 接口

```java
package com.example.llm.provider;

import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatStreamEvent;
import reactor.core.publisher.Flux;

public interface LlmStreamProviderClient {

    String provider();

    Flux<UnifiedChatStreamEvent> stream(UnifiedChatRequest request);
}
```
