# 修改 OpenAiCompatibleLlmClient

把 `chat()` 里的通用调用抽出来。

## 1. 增加 complete 方法

在 `OpenAiCompatibleLlmClient` 中新增：

```java
@Override
public String complete(String systemPrompt, String userPrompt) {
    ChatCompletionRequest request = new ChatCompletionRequest(
            properties.getModel(),
            List.of(
                    new ChatCompletionRequest.Message("system", systemPrompt),
                    new ChatCompletionRequest.Message("user", userPrompt)
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

        if (response == null || response.choices() == null || response.choices().isEmpty()) {
            throw new IllegalStateException("LLM response is empty");
        }

        ChatCompletionResponse.Choice firstChoice = response.choices().get(0);

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
```

---

## 2. 简化 chat 方法

把原来的 `chat()` 改成调用 `complete()`：

```java
@Override
public String chat(String message) {
    return complete(
            "你是一个严谨、简洁的 AI 应用开发助手。",
            message
    );
}
```

这样代码复用更好。
