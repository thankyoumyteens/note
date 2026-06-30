# AnthropicProviderClient

## AnthropicChatRequest

```java
package com.example.llm.dto.anthropic;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * Anthropic Messages API 请求体。
 * system 是顶层字段，messages 只放 user / assistant。
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record AnthropicChatRequest(
        String model, // 要调用的 Claude 模型名称。
        @JsonProperty("max_tokens")
        Integer maxTokens, // 限制模型最多生成的 token 数，只限制输出长度。
        Double temperature, // 控制模型输出随机性，值越低越稳定，值越高越发散。
        @JsonProperty("top_p")
        Double topP, // nucleus sampling 参数，用于控制候选 token 的采样范围。
        String system, // 系统指令，用于设置模型行为和回答边界。
        List<Message> messages, // 对话消息列表，只包含 user / assistant 消息。
        Boolean stream // 是否启用流式输出。
) {

    /**
     * Anthropic message。
     * role 只能是 user 或 assistant。
     */
    public record Message(
            String role, // 消息角色，只能是 user 或 assistant。
            String content // 消息文本内容。
    ) {
    }
}
```

## AnthropicChatStreamResponse

```java
package com.example.llm.dto.anthropic;

import com.example.llm.dto.TokenUsage;
import com.example.llm.exceptions.LlmProviderException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Anthropic Messages API Stream 的单个 SSE 事件。
 * Anthropic stream 是事件驱动结构，需要根据 event 名称解析不同 data。
 */
public record AnthropicChatStreamResponse(
        String event, // SSE event 名称，例如 message_start、content_block_delta、message_delta、message_stop。
        JsonNode root // SSE data 解析后的完整 JSON 节点。
) {

    /**
     * 将 SSE data 解析成 Anthropic stream 事件对象。
     */
    public static AnthropicChatStreamResponse parse(
            String provider,
            String event,
            String data,
            ObjectMapper objectMapper
    ) {
        try {
            return new AnthropicChatStreamResponse(
                    event,
                    objectMapper.readTree(data)
            );
        } catch (Exception ex) {
            throw new LlmProviderException(
                    provider,
                    -1,
                    "Failed to parse Anthropic stream chunk",
                    data,
                    ex
            );
        }
    }

    /**
     * 判断是否是 message_start 事件。
     */
    public boolean isMessageStart() {
        return "message_start".equals(event);
    }

    /**
     * 判断是否是 content_block_delta 事件。
     */
    public boolean isContentBlockDelta() {
        return "content_block_delta".equals(event);
    }

    /**
     * 判断是否是 message_delta 事件。
     */
    public boolean isMessageDelta() {
        return "message_delta".equals(event);
    }

    /**
     * 判断是否是 message_stop 事件。
     */
    public boolean isMessageStop() {
        return "message_stop".equals(event);
    }

    /**
     * 判断是否是 error 事件。
     */
    public boolean isError() {
        return "error".equals(event);
    }

    /**
     * 提取实际模型名称。
     * message_start 事件通常从 message.model 读取，其它事件没有则使用默认模型。
     */
    public String actualModel(String defaultModel) {
        String messageModel = root.path("message").path("model").asText("");

        if (!messageModel.isBlank()) {
            return messageModel;
        }

        String directModel = root.path("model").asText("");

        if (!directModel.isBlank()) {
            return directModel;
        }

        return defaultModel;
    }

    /**
     * 提取文本增量。
     * 只处理 delta.type = text_delta 的文本内容。
     */
    public String textDelta() {
        JsonNode delta = root.path("delta");

        if (!"text_delta".equals(delta.path("type").asText(""))) {
            return "";
        }

        return delta.path("text").asText("");
    }

    /**
     * 提取 token usage。
     * message_start 的 usage 在 message.usage 中，message_delta 的 usage 在根节点 usage 中。
     */
    public TokenUsage usage() {
        JsonNode usage = root.path("message").path("usage");

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
     * message_start 事件的 metadata。
     */
    public Map<String, Object> messageStartMetadata() {
        JsonNode message = root.path("message");
        JsonNode usage = message.path("usage");

        Map<String, Object> metadata = new LinkedHashMap<>();

        put(metadata, "event", event);
        put(metadata, "type", root.path("type").asText(""));
        put(metadata, "id", message.path("id").asText(""));
        put(metadata, "object", message.path("type").asText(""));
        put(metadata, "role", message.path("role").asText(""));
        put(metadata, "model", message.path("model").asText(""));
        put(metadata, "stopReason", message.path("stop_reason").asText(""));
        put(metadata, "stopSequence", message.path("stop_sequence").asText(""));

        if (!usage.isMissingNode() && !usage.isNull()) {
            put(metadata, "inputTokens", readInt(usage, "input_tokens"));
            put(metadata, "outputTokens", readInt(usage, "output_tokens"));
        }

        return Map.copyOf(metadata);
    }

    /**
     * content_block_delta 事件的 metadata。
     */
    public Map<String, Object> contentDeltaMetadata() {
        JsonNode delta = root.path("delta");

        Map<String, Object> metadata = new LinkedHashMap<>();

        put(metadata, "event", event);
        put(metadata, "type", root.path("type").asText(""));
        put(metadata, "index", readInt(root, "index"));
        put(metadata, "deltaType", delta.path("type").asText(""));

        return Map.copyOf(metadata);
    }

    /**
     * message_delta 事件的 metadata。
     */
    public Map<String, Object> messageDeltaMetadata() {
        JsonNode delta = root.path("delta");
        JsonNode usage = root.path("usage");

        Map<String, Object> metadata = new LinkedHashMap<>();

        put(metadata, "event", event);
        put(metadata, "type", root.path("type").asText(""));
        put(metadata, "stopReason", delta.path("stop_reason").asText(""));
        put(metadata, "stopSequence", delta.path("stop_sequence").asText(""));

        if (!usage.isMissingNode() && !usage.isNull()) {
            put(metadata, "outputTokens", readInt(usage, "output_tokens"));
        }

        return Map.copyOf(metadata);
    }

    /**
     * message_stop 事件的 metadata。
     * 会合并 message_delta 中保留的 stop reason / usage 等信息。
     */
    public Map<String, Object> messageStopMetadata(Map<String, Object> previousMetadata) {
        Map<String, Object> metadata = new LinkedHashMap<>();

        if (previousMetadata != null) {
            metadata.putAll(previousMetadata);
        }

        put(metadata, "event", event);
        put(metadata, "type", root.path("type").asText(""));

        return Map.copyOf(metadata);
    }

    /**
     * 提取 error 事件中的错误信息。
     */
    public String errorMessage(String fallbackMessage) {
        JsonNode error = root.path("error");

        String message = error.path("message").asText("");
        if (!message.isBlank()) {
            String type = error.path("type").asText("");
            return type.isBlank() ? message : type + ": " + message;
        }

        return fallbackMessage;
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
}
```

## AnthropicStreamProviderClient

```java
package com.example.llm.provider;

import com.example.llm.dto.LlmProvider;
import com.example.llm.dto.StreamEventType;
import com.example.llm.dto.TokenUsage;
import com.example.llm.dto.UnifiedChatMessage;
import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatStreamEvent;
import com.example.llm.dto.anthropic.AnthropicChatRequest;
import com.example.llm.dto.anthropic.AnthropicChatStreamResponse;
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
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeoutException;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;

/**
 * Anthropic Messages API stream provider。
 * 负责调用 Anthropic /messages 流式接口，并把 Anthropic SSE 事件转换成统一 stream event。
 */
public class AnthropicStreamProviderClient implements LlmStreamProviderClient {

    // SSE 响应的反序列化类型，用于读取 event: xxx / data: xxx 形式的流式事件。
    private static final ParameterizedTypeReference<ServerSentEvent<String>> SSE_STRING =
            new ParameterizedTypeReference<>() {
            };

    // provider 配置名称，例如 anthropic。
    private final String provider;

    // Anthropic API Key。
    private final String apiKey;

    // 当前 provider 要调用的模型名称。
    private final String model;

    // Anthropic API 版本，例如 2023-06-01。
    private final String anthropicVersion;

    // Anthropic Messages API 路径，通常是 /messages。
    private final String path;

    // stream 空闲超时时间，超过该时间没有收到事件就认为流中断。
    private final int streamIdleTimeoutSeconds;

    // 当前 provider 内部最大重试次数。
    private final int maxRetries;

    // 调用 Anthropic Messages API 的 WebClient。
    private final WebClient webClient;

    // 用于解析 Anthropic stream data。
    private final ObjectMapper objectMapper;

    public AnthropicStreamProviderClient(
            String provider,
            String baseUrl,
            String path,
            String apiKey,
            String model,
            String anthropicVersion,
            int streamIdleTimeoutSeconds,
            int maxRetries,
            int connectTimeoutMillis,
            int responseTimeoutSeconds,
            ObjectMapper objectMapper
    ) {
        this.provider = provider;
        this.apiKey = apiKey;
        this.model = model;
        this.anthropicVersion = anthropicVersion;
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
     * 发起 Anthropic Messages API 流式调用。
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
        // 把统一请求转换为 Anthropic Messages API 请求。
        AnthropicChatRequest providerRequest = toProviderRequest(request);

        // 保存实际返回的模型名，message_start 后可能比配置值更准确。
        AtomicReference<String> actualModel = new AtomicReference<>(model);

        // 保存最新 usage，message_start 和 message_delta 可能分阶段返回 token 信息。
        AtomicReference<TokenUsage> latestUsage = new AtomicReference<>(TokenUsage.empty());

        // 保存最新 metadata，最终 message_stop 时合并输出。
        AtomicReference<Map<String, Object>> latestMetadata = new AtomicReference<>(Map.of());

        return webClient.post()
                .uri(path)
                .header("x-api-key", apiKey)
                .header("anthropic-version", anthropicVersion)
                .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .accept(MediaType.TEXT_EVENT_STREAM)
                .bodyValue(providerRequest)
                .retrieve()
                // 将 HTTP 错误状态转换成统一 provider 异常。
                .onStatus(
                        HttpStatusCode::isError,
                        response -> toException(response, "Provider server error")
                )
                // 按 SSE 格式读取 Anthropic 的流式事件。
                .bodyToFlux(SSE_STRING)
                // stream 空闲超时控制，防止连接长时间无响应。
                .timeout(Duration.ofSeconds(streamIdleTimeoutSeconds))
                // 将 Anthropic 原始事件转换为统一 stream event。
                .flatMap(sse -> toUnifiedEvent(
                        sse,
                        contentStarted,
                        actualModel,
                        latestUsage,
                        latestMetadata
                ))
                // 收到统一 DONE 事件后结束下游流。
                .takeUntil(event -> event.type() == StreamEventType.DONE);
    }

    /**
     * 将统一请求转换为 Anthropic Messages API 请求。
     */
    private AnthropicChatRequest toProviderRequest(UnifiedChatRequest request) {
        List<AnthropicChatRequest.Message> messages = request.messages()
                .stream()
                .map(this::toAnthropicMessage)
                .toList();

        return new AnthropicChatRequest(
                model,
                request.options().maxTokens(),
                request.options().temperature(),
                request.options().topP(),
                request.system(),
                messages,
                true
        );
    }

    /**
     * 将统一消息角色转换为 Anthropic 消息角色。
     */
    private AnthropicChatRequest.Message toAnthropicMessage(UnifiedChatMessage message) {
        String role = switch (message.role()) {
            case USER -> "user";
            case ASSISTANT -> "assistant";
        };

        return new AnthropicChatRequest.Message(role, message.content());
    }

    /**
     * 将单个 Anthropic SSE 事件转换为统一 stream event。
     */
    private Mono<UnifiedChatStreamEvent> toUnifiedEvent(
            ServerSentEvent<String> sse,
            AtomicBoolean contentStarted,
            AtomicReference<String> actualModel,
            AtomicReference<TokenUsage> latestUsage,
            AtomicReference<Map<String, Object>> latestMetadata
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
            // 解析 Anthropic stream 事件。
            AnthropicChatStreamResponse response = AnthropicChatStreamResponse.parse(
                    provider,
                    event,
                    data,
                    objectMapper
            );

            // message_start：保存模型名、初始 usage 和 message 级 metadata。
            if (response.isMessageStart()) {
                actualModel.set(response.actualModel(model));
                latestUsage.set(mergeUsage(latestUsage.get(), response.usage()));
                latestMetadata.set(response.messageStartMetadata());
                return Mono.empty();
            }

            // content_block_delta：输出文本增量 MESSAGE。
            if (response.isContentBlockDelta()) {
                String text = response.textDelta();

                if (text == null || text.isEmpty()) {
                    return Mono.empty();
                }

                // 一旦输出过文本，就不再允许当前 provider retry。
                contentStarted.set(true);

                return Mono.just(UnifiedChatStreamEvent.message(
                        LlmProvider.ANTHROPIC,
                        actualModel.get(),
                        text,
                        response.contentDeltaMetadata()
                ));
            }

            // message_delta：保存 stop reason、stop sequence 和累计 usage。
            if (response.isMessageDelta()) {
                latestUsage.set(mergeUsage(latestUsage.get(), response.usage()));
                latestMetadata.set(response.messageDeltaMetadata());
                return Mono.empty();
            }

            // message_stop：输出 DONE，并携带最终 usage 和 metadata。
            if (response.isMessageStop()) {
                return Mono.just(UnifiedChatStreamEvent.done(
                        LlmProvider.ANTHROPIC,
                        actualModel.get(),
                        latestUsage.get(),
                        response.messageStopMetadata(latestMetadata.get())
                ));
            }

            // error：转换为统一 provider 异常。
            if (response.isError()) {
                return Mono.error(new LlmProviderException(
                        provider,
                        -1,
                        response.errorMessage("Anthropic stream error event"),
                        data
                ));
            }

            // content_block_start / content_block_stop / ping 等事件不输出给前端。
            return Mono.empty();

        } catch (LlmProviderException ex) {
            // 已经是统一 provider 异常，直接向外传递。
            return Mono.error(ex);

        } catch (Exception ex) {
            // 兜底保护，避免未知解析或转换错误丢失上下文。
            return Mono.error(new LlmProviderException(
                    provider,
                    -1,
                    "Failed to process Anthropic stream chunk",
                    data,
                    ex
            ));
        }
    }

    /**
     * 合并 Anthropic 分阶段返回的 usage。
     * 新 usage 中非空字段优先，缺失字段保留旧值。
     */
    private TokenUsage mergeUsage(TokenUsage current, TokenUsage incoming) {
        if (incoming == null) {
            return current == null ? TokenUsage.empty() : current;
        }

        Integer inputTokens = incoming.inputTokens() != null
                ? incoming.inputTokens()
                : current == null ? null : current.inputTokens();

        Integer outputTokens = incoming.outputTokens() != null
                ? incoming.outputTokens()
                : current == null ? null : current.outputTokens();

        return TokenUsage.of(inputTokens, outputTokens);
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
