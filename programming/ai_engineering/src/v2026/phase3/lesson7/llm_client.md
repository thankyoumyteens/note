# 修改 LlmClient

修改：

```text
client/LlmClient.java
```

改成：

```java
package com.example.aigateway.client;

import com.example.aigateway.dto.LlmCallType;
import reactor.core.publisher.Flux;

public interface LlmClient {

    String chat(String message);

    Flux<String> streamChat(String message);

    // 保留旧方法，避免已有代码大量修改
    default String complete(String systemPrompt, String userPrompt) {
        return complete(systemPrompt, userPrompt, LlmCallType.COMPLETE);
    }

    // 本课新增重载
    String complete(String systemPrompt, String userPrompt, LlmCallType callType);
}
```
