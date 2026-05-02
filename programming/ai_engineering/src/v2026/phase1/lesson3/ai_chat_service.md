# 修改 AiChatService

现在应该类似这样：

```java
package com.example.aigateway.service;

import com.example.aigateway.client.LlmClient;
import org.springframework.stereotype.Service;

@Service
public class AiChatService {

    private final LlmClient llmClient;

    public AiChatService(LlmClient llmClient) {
        this.llmClient = llmClient;
    }

    public String chat(String message) {
        if (message == null || message.isBlank()) {
            throw new IllegalArgumentException("message cannot be empty");
        }

        return llmClient.chat(message);
    }
}
```

改成：

```java
package com.example.aigateway.service;

import com.example.aigateway.client.LlmClient;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;

@Service
public class AiChatService {

    private final LlmClient llmClient;

    public AiChatService(LlmClient llmClient) {
        this.llmClient = llmClient;
    }

    public String chat(String message) {
        validateMessage(message);
        return llmClient.chat(message);
    }

    public Flux<String> streamChat(String message) {
        validateMessage(message);
        return llmClient.streamChat(message);
    }

    private void validateMessage(String message) {
        if (message == null || message.isBlank()) {
            throw new IllegalArgumentException("message cannot be empty");
        }
    }
}
```
