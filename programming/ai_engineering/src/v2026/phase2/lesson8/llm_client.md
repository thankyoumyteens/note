# 修改 LlmClient

文件：

```text
src/main/java/com/example/aigateway/client/LlmClient.java
```

```java
package com.example.aigateway.client;

import com.example.aigateway.dto.LlmCallType;
import reactor.core.publisher.Flux;

/**
 * 大模型调用统一抽象。
 */
public interface LlmClient {

    String chat(String message);

    Flux<String> streamChat(String message);

    /**
     * 兼容旧调用：默认使用 COMPLETE 类型。
     */
    default String complete(String systemPrompt, String userPrompt) {
        return complete(systemPrompt, userPrompt, LlmCallType.COMPLETE);
    }

    /**
     * 带调用类型的通用模型调用。
     */
    String complete(String systemPrompt, String userPrompt, LlmCallType callType);
}
```
