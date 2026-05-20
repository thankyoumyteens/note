# 修改 OpenAiCompatibleLlmClient

在 `OpenAiCompatibleLlmClient` 中新增 `complete` 方法。

文件：

```text
src/main/java/com/example/aigateway/client/openai/OpenAiCompatibleLlmClient.java
```

在类中加入：

```java
/**
 * 通用模型调用方法。
 *
 * 与 chat(message) 的区别：
 * - chat 使用固定 system prompt
 * - complete 允许调用方传入不同 system prompt
 *
 * 结构化输出、JSON 修复、工具调用决策等场景都应该用 complete。
 */
@Override
public String complete(String systemPrompt, String userPrompt) {
    ChatCompletionRequest request = new ChatCompletionRequest(
            properties.getModel(),
            List.of(
                    new ChatCompletionRequest.Message(
                            "system",
                            systemPrompt
                    ),
                    new ChatCompletionRequest.Message(
                            "user",
                            userPrompt
                    )
            ),
            0.1,
            false
    );

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
```

然后建议把 `chat` 方法改成复用 `complete`：

```java
/**
 * 普通聊天：使用默认 system prompt。
 */
@Override
public String chat(String message) {
    return complete(
            "你是一个严谨、简洁的 AI 应用开发助手。",
            message
    );
}
```

这样可以减少重复代码。
