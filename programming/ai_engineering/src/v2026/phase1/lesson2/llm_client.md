# 实现真实 LLM Client

先把第 1 课的 `MockLlmClient` 注释掉或删掉，否则 Spring 会发现两个 `LlmClient` 实现，启动时报错。

新建：

```text
client.openai/OpenAiCompatibleLlmClient.java
```

代码：

```java
package com.example.aigateway.client.openai;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.client.openai.dto.ChatCompletionRequest;
import com.example.aigateway.client.openai.dto.ChatCompletionResponse;
import com.example.aigateway.config.LlmProperties;
import java.util.List;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;

@Component
public class OpenAiCompatibleLlmClient implements LlmClient {

    private final WebClient llmWebClient;
    private final LlmProperties properties;

    public OpenAiCompatibleLlmClient(WebClient llmWebClient, LlmProperties properties) {
        this.llmWebClient = llmWebClient;
        this.properties = properties;
    }

    @Override
    public String chat(String message) {
        ChatCompletionRequest request = new ChatCompletionRequest(
                properties.getModel(),
                List.of(
                        new ChatCompletionRequest.Message(
                                "system",
                                "你是一个严谨、简洁的 AI 应用开发助手。"
                        ),
                        new ChatCompletionRequest.Message(
                                "user",
                                message
                        )
                ),
                0.3
        );

        try {
            ChatCompletionResponse response = llmWebClient.post()
                    .uri("/v1/chat/completions")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(ChatCompletionResponse.class)
                    .block();

            if (response == null || response.choices() == null || response.choices().isEmpty()) {
                throw new IllegalStateException("LLM response is empty");
            }

            ChatCompletionResponse.Choice firstChoice = response.choices().getFirst();

            if (firstChoice.message() == null || firstChoice.message().content() == null) {
                throw new IllegalStateException("LLM response message is empty");
            }

            return firstChoice.message().content().strip();

        } catch (WebClientResponseException e) {
            throw new RuntimeException(
                    "LLM API error. status=" + e.getStatusCode() +
                            ", body=" + e.getResponseBodyAsString(),
                    e
            );
        } catch (Exception e) {
            throw new RuntimeException("Failed to call LLM API: " + e.getMessage(), e);
        }
    }
}
```

注意这一行：

```java
ChatCompletionResponse.Choice firstChoice = response.choices().getFirst();
```

如果你的 Java 版本低于 21，`List#getFirst()` 不可用，改成：

```java
ChatCompletionResponse.Choice firstChoice = response.choices().get(0);
```

---

当模型 API 返回 4xx 或 5xx 时，WebClient 会抛出：

```java
WebClientResponseException
```

例如：

- 401 Unauthorized：API Key 错误
- 404 Not Found：base-url 或路径错误
- 429 Too Many Requests：限流
- 500：供应商内部错误
