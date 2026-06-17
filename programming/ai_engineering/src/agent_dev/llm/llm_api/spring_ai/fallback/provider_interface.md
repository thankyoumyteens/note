# 统一 ProviderClient 接口

```java
package com.example.llm.client;

import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatResponse;

/**
 * 所有 provider 的统一接口。
 */
public interface LlmProviderClient {

    String provider();

    UnifiedChatResponse chat(UnifiedChatRequest request);
}
```
