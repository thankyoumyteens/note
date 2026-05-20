# 实现 streamChat

文件：

```text
src/main/java/com/example/aigateway/client/openai/OpenAiCompatibleLlmClient.java
```

完整示例：

```java
package com.example.aigateway.client.openai;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.client.openai.dto.ChatCompletionChunk;
import com.example.aigateway.client.openai.dto.ChatCompletionRequest;
import com.example.aigateway.client.openai.dto.ChatCompletionResponse;
import com.example.aigateway.config.LlmProperties;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.List;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientResponseException;
import reactor.core.publisher.Flux;

/**
 * OpenAI-compatible 模型客户端。
 *
 * 当前职责：
 * - 普通非流式聊天
 * - 流式聊天
 *
 * 注意：
 * 业务层只依赖 LlmClient，不直接依赖这个类。
 */
@Component
public class OpenAiCompatibleLlmClient implements LlmClient {

    private final WebClient llmWebClient;
    private final LlmProperties properties;
    private final ObjectMapper objectMapper;

    public OpenAiCompatibleLlmClient(
            WebClient llmWebClient,
            LlmProperties properties,
            ObjectMapper objectMapper
    ) {
        this.llmWebClient = llmWebClient;
        this.properties = properties;
        this.objectMapper = objectMapper;
    }

    /**
     * 普通聊天：等待模型完整生成后，一次性返回。
     */
    @Override
    public String chat(String message) {
        ChatCompletionRequest request = buildRequest(message, false);

        try {
            ChatCompletionResponse response = llmWebClient.post()
                    .uri("/v1/chat/completions")
                    .bodyValue(request)
                    .retrieve()
                    .bodyToMono(ChatCompletionResponse.class)
                    .block();

            if (response == null
                    || response.choices() == null
                    || response.choices().isEmpty()) {
                throw new IllegalStateException("LLM response is empty");
            }

            ChatCompletionResponse.Choice firstChoice = response.choices().get(0);

            if (firstChoice.message() == null
                    || firstChoice.message().content() == null) {
                throw new IllegalStateException("LLM response message is empty");
            }

            return firstChoice.message().content().strip();

        } catch (WebClientResponseException e) {
            throw new RuntimeException(
                    "LLM API error. status=" + e.getStatusCode()
                            + ", body=" + e.getResponseBodyAsString(),
                    e
            );
        } catch (Exception e) {
            throw new RuntimeException("Failed to call LLM API: " + e.getMessage(), e);
        }
    }

    /**
     * 流式聊天：模型边生成边返回。
     *
     * 返回 Flux<String>，每个 String 是模型新增的一小段文本。
     */
    @Override
    public Flux<String> streamChat(String message) {
        ChatCompletionRequest request = buildRequest(message, true);

        return llmWebClient.post()
                .uri("/v1/chat/completions")
                .accept(MediaType.TEXT_EVENT_STREAM)
                .bodyValue(request)
                .retrieve()
                .bodyToFlux(String.class)
                .flatMap(this::parseSseChunk)
                .onErrorResume(e -> Flux.just("[ERROR] " + e.getMessage()));
    }

    /**
     * 构建 Chat Completions 请求。
     *
     * stream = false：普通调用
     * stream = true：流式调用
     */
    private ChatCompletionRequest buildRequest(String message, boolean stream) {
        return new ChatCompletionRequest(
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
                0.3,
                stream
        );
    }

    /**
     * 解析模型返回的 SSE chunk。
     *
     * 供应商可能返回：
     * data: {"choices":[{"delta":{"content":"RAG"}}]}
     *
     * 也可能 WebClient 已经帮你拆掉 data: 前缀，只剩：
     * {"choices":[{"delta":{"content":"RAG"}}]}
     */
    private Flux<String> parseSseChunk(String rawChunk) {
        try {
            if (rawChunk == null || rawChunk.isBlank()) {
                return Flux.empty();
            }

            String text = rawChunk.strip();

            // OpenAI-compatible 流式响应最后通常会返回 [DONE]
            if ("[DONE]".equals(text) || "data: [DONE]".equals(text)) {
                return Flux.empty();
            }

            // 如果还有 data: 前缀，就手动去掉
            if (text.startsWith("data:")) {
                text = text.substring("data:".length()).strip();
            }

            if (text.isBlank() || "[DONE]".equals(text)) {
                return Flux.empty();
            }

            ChatCompletionChunk chunk = objectMapper.readValue(
                    text,
                    ChatCompletionChunk.class
            );

            if (chunk.choices() == null || chunk.choices().isEmpty()) {
                return Flux.empty();
            }

            ChatCompletionChunk.Choice choice = chunk.choices().get(0);

            if (choice.delta() == null || choice.delta().content() == null) {
                return Flux.empty();
            }

            return Flux.just(choice.delta().content());

        } catch (Exception e) {
            // 某些供应商可能会返回非标准 chunk。
            // 当前学习阶段先忽略解析失败的 chunk，避免整个流中断。
            return Flux.empty();
        }
    }
}
```

## `bodyToFlux(String.class)` 的含义

第 2 课普通响应使用：

```java
.bodyToMono(ChatCompletionResponse.class)
```

意思是读取一个完整响应。

第 3 课流式响应使用：

```java
.bodyToFlux(String.class)
```

意思是读取多个字符串片段。

对比：

```text
Mono<T>：一个结果
Flux<T>：多个结果
```

这里每个 `String` 可能是一段 SSE 数据。

## 一个重要说明：bodyToFlux(String.class) 的兼容问题

不同供应商对 SSE 的返回格式略有差异。

有的 `bodyToFlux(String.class)` 得到的是：

```text
{"choices":[{"delta":{"content":"RAG"}}]}
```

有的得到的是：

```text
data: {"choices":[{"delta":{"content":"RAG"}}]}
```

所以我在 `parseSseChunk` 里兼容了：

```java
if (chunk.startsWith("data:")) {
    chunk = chunk.substring("data:".length()).strip();
}
```

如果你的供应商返回格式更特殊，可以自行根据你的实际返回调整。
