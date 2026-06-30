# OpenAiResponsesProviderClient

## OpenAiResponsesRequest

```java
package com.example.llm.dto.openai;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * OpenAI Responses API 请求体。
 * input 这里使用 messages 数组，方便兼容多轮对话历史。
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record OpenAiResponsesRequest(
        String model, // 要调用的模型名称。
        String instructions, // system / developer 类指令，用于设置模型行为和回答边界。
        List<ResponseInputMessage> input, // 输入消息列表，用于承载 user / assistant 多轮对话历史。
        Double temperature, // 控制模型输出随机性，值越低越稳定，值越高越发散。

        @JsonProperty("max_output_tokens")
        Integer maxOutputTokens, // 限制模型最多生成的 token 数，只限制输出长度。

        Boolean stream, // 是否启用流式输出。

        @JsonProperty("previous_response_id")
        String previousResponseId // 上一轮 response id，用于让 Responses API 续接上下文。
) {

    /**
     * Responses API 的输入消息。
     * role 通常是 user / assistant。
     */
    public record ResponseInputMessage(
            String role, // 消息角色，通常是 user 或 assistant。
            String content // 消息文本内容。
    ) {
    }
}
```

## OpenAiResponsesStreamResponse

```java
package com.example.llm.dto.openai;

import com.example.llm.dto.TokenUsage;
import com.example.llm.exceptions.LlmProviderException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * OpenAI Responses API Stream 的单个 SSE 事件。
 * Responses API 是事件驱动结构，不能复用 Chat Completions 的 choices[].delta DTO。
 */
public record OpenAiResponsesStreamResponse(
        String event, // SSE event 名称，例如 response.output_text.delta、response.completed。
        JsonNode root // SSE data 解析后的完整 JSON 节点。
) {

    /**
     * 将 SSE data 解析成 Responses stream 事件对象。
     */
    public static OpenAiResponsesStreamResponse parse(
            String provider,
            String event,
            String data,
            ObjectMapper objectMapper
    ) {
        try {
            return new OpenAiResponsesStreamResponse(
                    event,
                    objectMapper.readTree(data)
            );
        } catch (Exception ex) {
            throw new LlmProviderException(
                    provider,
                    -1,
                    "Failed to parse OpenAI Responses stream chunk",
                    data,
                    ex
            );
        }
    }

    /**
     * 判断是否是文本增量事件。
     */
    public boolean isOutputTextDelta() {
        return "response.output_text.delta".equals(event);
    }

    /**
     * 判断是否是最终完成事件。
     */
    public boolean isCompleted() {
        return "response.completed".equals(event);
    }

    /**
     * 判断是否是失败事件。
     */
    public boolean isFailed() {
        return "response.failed".equals(event);
    }

    /**
     * 判断是否是未完整完成事件。
     */
    public boolean isIncomplete() {
        return "response.incomplete".equals(event);
    }

    /**
     * 判断是否是通用错误事件。
     */
    public boolean isError() {
        return "error".equals(event);
    }

    /**
     * 提取文本增量。
     */
    public String deltaText() {
        return root.path("delta").asText("");
    }

    /**
     * 提取实际模型名称。
     * response.completed 事件通常从 response.model 读取，其它事件没有则使用默认模型。
     */
    public String actualModel(String defaultModel) {
        String responseModel = root.path("response").path("model").asText("");

        if (!responseModel.isBlank()) {
            return responseModel;
        }

        String directModel = root.path("model").asText("");

        if (!directModel.isBlank()) {
            return directModel;
        }

        return defaultModel;
    }

    /**
     * 从 response.completed 事件中提取 token usage。
     */
    public TokenUsage usage() {
        JsonNode usage = root.path("response").path("usage");

        if (usage.isMissingNode() || usage.isNull()) {
            usage = root.path("usage");
        }

        if (usage.isMissingNode() || usage.isNull()) {
            return TokenUsage.empty();
        }

        Integer inputTokens = readInt(usage, "input_tokens");
        Integer outputTokens = readInt(usage, "output_tokens");

        return TokenUsage.of(inputTokens, outputTokens);
    }

    /**
     * 文本增量事件的 metadata。
     */
    public Map<String, Object> deltaMetadata() {
        Map<String, Object> metadata = new LinkedHashMap<>();

        put(metadata, "event", event);
        put(metadata, "type", root.path("type").asText(""));
        put(metadata, "sequenceNumber", readLong(root, "sequence_number"));
        put(metadata, "itemId", root.path("item_id").asText(""));
        put(metadata, "outputIndex", readInt(root, "output_index"));
        put(metadata, "contentIndex", readInt(root, "content_index"));

        return Map.copyOf(metadata);
    }

    /**
     * response.completed 事件的 metadata。
     */
    public Map<String, Object> completedMetadata() {
        JsonNode response = root.path("response");

        Map<String, Object> metadata = new LinkedHashMap<>();

        put(metadata, "event", event);
        put(metadata, "type", root.path("type").asText(""));
        put(metadata, "sequenceNumber", readLong(root, "sequence_number"));

        put(metadata, "id", response.path("id").asText(""));
        put(metadata, "object", response.path("object").asText(""));
        put(metadata, "createdAt", readLong(response, "created_at"));
        put(metadata, "completedAt", readLong(response, "completed_at"));
        put(metadata, "status", response.path("status").asText(""));
        put(metadata, "model", response.path("model").asText(""));
        put(metadata, "previousResponseId", response.path("previous_response_id").asText(""));
        put(metadata, "maxOutputTokens", readInt(response, "max_output_tokens"));
        put(metadata, "temperature", readDouble(response, "temperature"));
        put(metadata, "topP", readDouble(response, "top_p"));
        put(metadata, "truncation", response.path("truncation").asText(""));
        put(metadata, "toolChoice", response.path("tool_choice").asText(""));

        JsonNode usage = response.path("usage");
        if (!usage.isMissingNode() && !usage.isNull()) {
            put(metadata, "inputTokens", readInt(usage, "input_tokens"));
            put(metadata, "outputTokens", readInt(usage, "output_tokens"));
            put(metadata, "totalTokens", readInt(usage, "total_tokens"));

            JsonNode outputTokenDetails = usage.path("output_tokens_details");
            if (!outputTokenDetails.isMissingNode() && !outputTokenDetails.isNull()) {
                put(metadata, "reasoningTokens", readInt(outputTokenDetails, "reasoning_tokens"));
            }
        }

        JsonNode providerMetadata = response.path("metadata");
        if (!providerMetadata.isMissingNode() && !providerMetadata.isNull() && providerMetadata.isObject()) {
            put(metadata, "providerMetadata", providerMetadata);
        }

        return Map.copyOf(metadata);
    }

    /**
     * 提取 failed / error 事件中的错误信息。
     */
    public String errorMessage(String fallbackMessage) {
        JsonNode responseError = root.path("response").path("error");

        String responseErrorMessage = responseError.path("message").asText("");
        if (!responseErrorMessage.isBlank()) {
            String code = responseError.path("code").asText("");
            return code.isBlank() ? responseErrorMessage : code + ": " + responseErrorMessage;
        }

        JsonNode directError = root.path("error");

        String directErrorMessage = directError.path("message").asText("");
        if (!directErrorMessage.isBlank()) {
            String code = directError.path("code").asText("");
            return code.isBlank() ? directErrorMessage : code + ": " + directErrorMessage;
        }

        return fallbackMessage;
    }

    /**
     * 提取 incomplete 事件中的原因。
     */
    public String incompleteMessage() {
        JsonNode details = root.path("response").path("incomplete_details");
        String reason = details.path("reason").asText("");

        if (!reason.isBlank()) {
            return "OpenAI Responses stream incomplete: " + reason;
        }

        return "OpenAI Responses stream incomplete";
    }

    private void put(Map<String, Object> metadata, String key, Object value) {
        if (value == null) {
            return;
        }

        if (value instanceof String text && text.isBlank()) {
            return;
        }

        metadata.put(key, value);
    }

    private Integer readInt(JsonNode node, String fieldName) {
        JsonNode value = node.path(fieldName);
        return value.isNumber() ? value.asInt() : null;
    }

    private Long readLong(JsonNode node, String fieldName) {
        JsonNode value = node.path(fieldName);
        return value.isNumber() ? value.asLong() : null;
    }

    private Double readDouble(JsonNode node, String fieldName) {
        JsonNode value = node.path(fieldName);
        return value.isNumber() ? value.asDouble() : null;
    }
}
```

## OpenAiResponsesStreamProviderClient

```java
package com.example.llm.provider;

import com.example.llm.dto.*;
import com.example.llm.dto.openai.OpenAiResponsesRequest;
import com.example.llm.dto.openai.OpenAiResponsesStreamResponse;
import com.example.llm.exceptions.LlmProviderException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientRequestException;
import reactor.core.Exceptions;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.util.retry.Retry;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeoutException;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * OpenAI Responses API stream provider。
 * 负责调用 /responses 流式接口，并把 Responses API 的 SSE 事件转换成统一 stream event。
 */
public class OpenAiResponsesStreamProviderClient implements LlmStreamProviderClient {

    // SSE 响应的反序列化类型，用于读取 event: xxx / data: xxx 形式的流式事件。
    private static final ParameterizedTypeReference<ServerSentEvent<String>> SSE_STRING =
            new ParameterizedTypeReference<>() {
            };

    // provider 配置名称，例如 openai-responses。
    private final String provider;

    // OpenAI API Key。
    private final String apiKey;

    // 当前 provider 要调用的模型名称。
    private final String model;

    // Responses API 路径，通常是 /responses。
    private final String path;

    // stream 空闲超时时间，超过该时间没有收到事件就认为流中断。
    private final int streamIdleTimeoutSeconds;

    // 当前 provider 内部最大重试次数。
    private final int maxRetries;

    // 调用 OpenAI Responses API 的 WebClient。
    private final WebClient webClient;

    // 用于解析 Responses API stream data。
    private final ObjectMapper objectMapper;

    public OpenAiResponsesStreamProviderClient(
            String provider,
            String baseUrl,
            String path,
            String apiKey,
            String model,
            int streamIdleTimeoutSeconds,
            int maxRetries,
            int connectTimeoutMillis,
            int responseTimeoutSeconds,
            ObjectMapper objectMapper
    ) {
        this.provider = provider;
        this.apiKey = apiKey;
        this.model = model;
        this.path = path;
        this.streamIdleTimeoutSeconds = streamIdleTimeoutSeconds;
        this.maxRetries = maxRetries;
        this.webClient = WebClientFactory.create(baseUrl, connectTimeoutMillis, responseTimeoutSeconds);
        this.objectMapper = objectMapper;
    }

    /**
     * 返回当前 ProviderClient 的配置名称。
     */
    @Override
    public String provider() {
        return provider;
    }

    /**
     * 发起 Responses API 流式调用。
     * 如果尚未输出任何文本，并且异常可重试，则在当前 provider 内部 retry。
     */
    @Override
    public Flux<UnifiedChatStreamEvent> stream(UnifiedChatRequest request) {
        // 标记当前 provider 是否已经输出过 message chunk。
        AtomicBoolean contentStarted = new AtomicBoolean(false);

        // defer 保证每次 subscribe / retry 时重新创建一次 WebClient stream 请求。
        return Flux.defer(() -> doStream(request, contentStarted))
                .retryWhen(
                        Retry.backoff(maxRetries, Duration.ofMillis(500))
                                // 限制最大退避时间，避免重试等待过久。
                                .maxBackoff(Duration.ofSeconds(3))
                                // 增加随机抖动，避免多个请求同时重试造成尖峰。
                                .jitter(0.2)
                                // 只有尚未输出内容，并且异常可重试时，才允许 retry。
                                .filter(ex -> !contentStarted.get() && isRetryable(ex))
                                // 重试耗尽后，把最后一次异常继续向外抛出。
                                .onRetryExhaustedThrow((spec, signal) -> signal.failure())
                );
    }

    /**
     * 执行真正的 WebClient stream 请求。
     */
    private Flux<UnifiedChatStreamEvent> doStream(
            UnifiedChatRequest request,
            AtomicBoolean contentStarted
    ) {
        // 把统一请求转换为 OpenAI Responses API 请求。
        OpenAiResponsesRequest providerRequest = toProviderRequest(request);

        return webClient.post()
                .uri(path)
                .header(HttpHeaders.AUTHORIZATION, "Bearer " + apiKey)
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.TEXT_EVENT_STREAM)
                .bodyValue(providerRequest)
                .retrieve()
                // 将 HTTP 错误状态转换成统一 provider 异常。
                .onStatus(
                        HttpStatusCode::isError,
                        response -> toException(response, "Provider server error")
                )
                // 按 SSE 格式读取 Responses API 的流式事件。
                .bodyToFlux(SSE_STRING)
                // stream 空闲超时控制，防止连接长时间无响应。
                .timeout(Duration.ofSeconds(streamIdleTimeoutSeconds))
                // 将 Responses API 原始事件转换为统一 stream event。
                .flatMap(sse -> toUnifiedEvent(sse, contentStarted))
                // 收到统一 DONE 事件后结束下游流。
                .takeUntil(event -> event.type() == StreamEventType.DONE);
    }

    /**
     * 将统一请求转换为 Responses API 请求。
     */
    private OpenAiResponsesRequest toProviderRequest(UnifiedChatRequest request) {
        List<OpenAiResponsesRequest.ResponseInputMessage> input = new ArrayList<>();

        // Responses API 的 input 可以承载多轮 user / assistant 历史消息。
        for (UnifiedChatMessage message : request.messages()) {
            input.add(new OpenAiResponsesRequest.ResponseInputMessage(
                    toResponseRole(message.role()),
                    message.content()
            ));
        }

        return new OpenAiResponsesRequest(
                model,
                request.system(),
                input,
                request.options().temperature(),
                request.options().maxTokens(),
                true,
                null
        );
    }

    /**
     * 将业务层角色枚举映射成 Responses API 使用的 role 字符串。
     */
    private String toResponseRole(ChatRole role) {
        return switch (role) {
            case USER -> "user";
            case ASSISTANT -> "assistant";
        };
    }

    /**
     * 将单个 Responses API SSE 事件转换为统一 stream event。
     */
    private Mono<UnifiedChatStreamEvent> toUnifiedEvent(
            ServerSentEvent<String> sse,
            AtomicBoolean contentStarted
    ) {
        String event = sse.event();
        String data = sse.data();

        // 没有事件名的 SSE 不处理。
        if (event == null || event.isBlank()) {
            return Mono.empty();
        }

        // 没有 data 的 SSE 不处理。
        if (data == null || data.isBlank()) {
            return Mono.empty();
        }

        try {
            // 解析 Responses API stream 事件。
            OpenAiResponsesStreamResponse response = OpenAiResponsesStreamResponse.parse(
                    provider,
                    event,
                    data,
                    objectMapper
            );

            // 文本增量事件：输出 MESSAGE。
            if (response.isOutputTextDelta()) {
                String delta = response.deltaText();

                if (delta.isEmpty()) {
                    return Mono.empty();
                }

                // 一旦输出过文本，就不再允许当前 provider retry。
                contentStarted.set(true);

                return Mono.just(UnifiedChatStreamEvent.message(
                        LlmProvider.OPENAI,
                        response.actualModel(model),
                        delta,
                        response.deltaMetadata()
                ));
            }

            // 完成事件：输出 DONE，并保留 usage 和 response 级元数据。
            if (response.isCompleted()) {
                return Mono.just(UnifiedChatStreamEvent.done(
                        LlmProvider.OPENAI,
                        response.actualModel(model),
                        response.usage(),
                        response.completedMetadata()
                ));
            }

            // 失败事件：转换为统一 provider 异常。
            if (response.isFailed()) {
                return Mono.error(new LlmProviderException(
                        provider,
                        -1,
                        response.errorMessage("OpenAI Responses stream failed"),
                        data
                ));
            }

            // 未完整完成事件：转换为统一 provider 异常。
            if (response.isIncomplete()) {
                return Mono.error(new LlmProviderException(
                        provider,
                        -1,
                        response.incompleteMessage(),
                        data
                ));
            }

            // 通用错误事件：转换为统一 provider 异常。
            if (response.isError()) {
                return Mono.error(new LlmProviderException(
                        provider,
                        -1,
                        response.errorMessage("OpenAI Responses stream error event"),
                        data
                ));
            }

            // response.created / response.in_progress / response.output_text.done 等事件不输出给前端。
            // 注意：不能在 response.output_text.done 时结束，因为 usage 通常要等 response.completed。
            return Mono.empty();

        } catch (LlmProviderException ex) {
            // 已经是统一 provider 异常，直接向外传递。
            return Mono.error(ex);

        } catch (Exception ex) {
            // 兜底保护，避免未知解析或转换错误丢失上下文。
            return Mono.error(new LlmProviderException(
                    provider,
                    -1,
                    "Failed to process OpenAI Responses stream chunk",
                    data,
                    ex
            ));
        }
    }

    /**
     * 将 HTTP 错误响应转换为统一 provider 异常。
     */
    private Mono<? extends Throwable> toException(ClientResponse response, String message) {
        return response.bodyToMono(String.class)
                .defaultIfEmpty("")
                .map(body -> new LlmProviderException(
                        provider,
                        response.statusCode().value(),
                        message,
                        body
                ));
    }

    /**
     * 判断异常是否允许在当前 provider 内部重试。
     */
    private boolean isRetryable(Throwable throwable) {
        Throwable ex = Exceptions.unwrap(throwable);

        // Reactor timeout 会表现为 TimeoutException。
        if (ex instanceof TimeoutException) {
            return true;
        }

        // 网络连接失败、DNS 失败、连接被拒绝等通常会表现为 WebClientRequestException。
        if (ex instanceof WebClientRequestException) {
            return true;
        }

        if (ex instanceof LlmProviderException providerException) {
            int status = providerException.statusCode();

            // -1 表示非 HTTP 状态错误，例如网络异常包装、stream error event 或解析失败等。
            return status == -1
                    || status == 429
                    || status == 500
                    || status == 502
                    || status == 503
                    || status == 504;
        }

        return false;
    }
}
```
