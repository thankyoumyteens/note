# 统一 ProviderClient 接口

```java
package com.example.llm.provider;

import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatResponse;
import reactor.core.publisher.Mono;

public interface LlmProviderClient {

    String provider();

    Mono<UnifiedChatResponse> chat(UnifiedChatRequest request);
}
```
