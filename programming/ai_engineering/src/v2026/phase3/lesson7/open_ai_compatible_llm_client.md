# 修改 OpenAiCompatibleLlmClient

## 修改 OpenAiCompatibleLlmClient 构造器

给 `OpenAiCompatibleLlmClient` 注入 `LlmCallLogService`。

```java
private final LlmCallLogService llmCallLogService;
```

构造器增加参数：

```java
public OpenAiCompatibleLlmClient(
        WebClient llmWebClient,
        LlmProperties properties,
        ObjectMapper objectMapper,
        LlmCallLogService llmCallLogService
) {
    this.llmWebClient = llmWebClient;
    this.properties = properties;
    this.objectMapper = objectMapper;
    this.llmCallLogService = llmCallLogService;
}
```

需要 import：

```java
import com.example.aigateway.service.LlmCallLogService;
```

## 修改 chat 方法

原来：

```java
@Override
public String chat(String message) {
    return complete(
            "你是一个严谨、简洁的 AI 应用开发助手。",
            message
    );
}
```

改成：

```java
@Override
public String chat(String message) {
    return complete(
            "你是一个严谨、简洁的 AI 应用开发助手。",
            message,
            LlmCallType.CHAT
    );
}
```

需要 import：

```java
import com.example.aigateway.dto.LlmCallType;
```

## 修改 complete 方法记录日志

把原来的：

```java
@Override
public String complete(String systemPrompt, String userPrompt) {
    ...
}
```

改成：

```java
@Override
public String complete(String systemPrompt, String userPrompt, LlmCallType callType) {
    long start = System.currentTimeMillis();

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

        long latencyMs = System.currentTimeMillis() - start;

        if (response == null || response.choices() == null || response.choices().isEmpty()) {
            llmCallLogService.recordFailure(
                    callType,
                    properties.getModel(),
                    latencyMs,
                    "LLM response is empty"
            );
            throw new IllegalStateException("LLM response is empty");
        }

        ChatCompletionResponse.Choice firstChoice = response.choices().get(0);

        if (firstChoice.message() == null || firstChoice.message().content() == null) {
            llmCallLogService.recordFailure(
                    callType,
                    properties.getModel(),
                    latencyMs,
                    "LLM response message is empty"
            );
            throw new IllegalStateException("LLM response message is empty");
        }

        ChatCompletionResponse.Usage usage = response.usage();

        llmCallLogService.recordSuccess(
                callType,
                properties.getModel(),
                latencyMs,
                usage == null ? null : usage.prompt_tokens(),
                usage == null ? null : usage.completion_tokens(),
                usage == null ? null : usage.total_tokens()
        );

        return firstChoice.message().content().strip();

    } catch (WebClientResponseException e) {
        long latencyMs = System.currentTimeMillis() - start;

        llmCallLogService.recordFailure(
                callType,
                properties.getModel(),
                latencyMs,
                "LLM API error. status=" + e.getStatusCode()
        );

        throw new RuntimeException(
                "LLM API error. status=" + e.getStatusCode() +
                        ", body=" + e.getResponseBodyAsString(),
                e
        );
    } catch (Exception e) {
        long latencyMs = System.currentTimeMillis() - start;

        llmCallLogService.recordFailure(
                callType,
                properties.getModel(),
                latencyMs,
                e.getMessage()
        );

        throw new RuntimeException("Failed to call LLM API: " + e.getMessage(), e);
    }
}
```

注意：这个版本会让所有 `complete()` 调用都被记录。

## 修改 streamChat 方法记录日志

流式响应通常不一定能拿到 usage，因此先记录：

```text
callType = STREAM_CHAT
token = null
success / failure
latencyMs
```

在 `streamChat` 中加基础日志：

```java
@Override
public Flux<String> streamChat(String message) {
    long start = System.currentTimeMillis();

    ChatCompletionRequest request = buildRequest(message, true);

    return llmWebClient.post()
            .uri("/v1/chat/completions")
            .bodyValue(request)
            .retrieve()
            .bodyToFlux(String.class)
            .flatMap(this::parseSseChunk)
            .doOnComplete(() -> llmCallLogService.recordSuccess(
                    LlmCallType.STREAM_CHAT,
                    properties.getModel(),
                    System.currentTimeMillis() - start,
                    null,
                    null,
                    null
            ))
            .doOnError(e -> llmCallLogService.recordFailure(
                    LlmCallType.STREAM_CHAT,
                    properties.getModel(),
                    System.currentTimeMillis() - start,
                    e.getMessage()
            ))
            .onErrorResume(e -> Flux.just("[ERROR] " + e.getMessage()));
}
```
