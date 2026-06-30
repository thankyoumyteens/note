# Controller 使用方式

## StreamEventResponse DTO

```java
package com.example.llm.dto;

/**
 * 返回给前端的 SSE JSON 数据。
 */
public record StreamEventResponse(
        String content, // message 事件中的增量文本内容。
        String code, // error 事件中的错误码。
        String message, // error 事件中的安全错误提示。
        Boolean done // 是否表示流式响应已经结束。
) {

    public static StreamEventResponse messageEvent(String content) {
        return new StreamEventResponse(content, "", "", false);
    }

    public static StreamEventResponse error(String code, String message) {
        return new StreamEventResponse("", code, message, false);
    }

    public static StreamEventResponse doneEvent() {
        return new StreamEventResponse("", "", "", true);
    }

    public static StreamEventResponse heartbeat() {
        return new StreamEventResponse("", "", "", false);
    }
}
```

## LlmStreamController.java

```java
package com.example.llm.controller;

import com.example.llm.dto.StreamEventResponse;
import com.example.llm.dto.StreamEventType;
import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatStreamEvent;
import com.example.llm.exceptions.AllProvidersFailedException;
import com.example.llm.exceptions.LlmProviderException;
import com.example.llm.provider.StreamProviderFallbackRouter;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

import java.time.Duration;

/**
 * SSE stream Controller。
 * Controller 只负责把统一 stream event 转成前端 SSE 事件。
 */
@RestController
@RequestMapping("/api/llm")
public class LlmStreamController {

    private final StreamProviderFallbackRouter router;

    public LlmStreamController(StreamProviderFallbackRouter router) {
        this.router = router;
    }

    @PostMapping(value = "/chat/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<StreamEventResponse>> stream(
            @RequestBody UnifiedChatRequest request
    ) {
        Flux<ServerSentEvent<StreamEventResponse>> contentEvents = router.stream(request)
                .map(this::toSseEvent);

        Flux<ServerSentEvent<StreamEventResponse>> heartbeatEvents = Flux.interval(Duration.ofSeconds(15))
                .map(tick -> ServerSentEvent.<StreamEventResponse>builder(StreamEventResponse.heartbeat())
                        .event("heartbeat")
                        .build());

        return Flux.merge(contentEvents, heartbeatEvents)
                // 一旦输出 done 事件，立即结束整个 SSE 流。
                .takeUntil(sse -> "done".equals(sse.event()))
                .onErrorResume(ex -> Flux.just(toErrorEvent(ex), doneEvent()));
    }

    private ServerSentEvent<StreamEventResponse> toSseEvent(UnifiedChatStreamEvent event) {
        if (event.type() == StreamEventType.MESSAGE) {
            return ServerSentEvent.<StreamEventResponse>builder(StreamEventResponse.messageEvent(event.content()))
                    .event("message")
                    .build();
        }

        if (event.type() == StreamEventType.DONE) {
            return doneEvent();
        }

        if (event.type() == StreamEventType.ERROR) {
            return ServerSentEvent.<StreamEventResponse>builder(
                            StreamEventResponse.error(event.errorCode(), event.errorMessage())
                    )
                    .event("error")
                    .build();
        }

        return ServerSentEvent.<StreamEventResponse>builder(StreamEventResponse.heartbeat())
                .event("heartbeat")
                .build();
    }

    private ServerSentEvent<StreamEventResponse> toErrorEvent(Throwable ex) {
        return ServerSentEvent.<StreamEventResponse>builder(
                        StreamEventResponse.error(toErrorCode(ex), toSafeMessage(ex))
                )
                .event("error")
                .build();
    }

    private ServerSentEvent<StreamEventResponse> doneEvent() {
        return ServerSentEvent.<StreamEventResponse>builder(StreamEventResponse.doneEvent())
                .event("done")
                .build();
    }

    private String toErrorCode(Throwable ex) {
        if (ex instanceof AllProvidersFailedException) {
            return "LLM_ALL_PROVIDERS_FAILED";
        }

        if (ex instanceof LlmProviderException providerException) {
            return switch (providerException.statusCode()) {
                case 400 -> "LLM_BAD_REQUEST";
                case 401 -> "LLM_UNAUTHORIZED";
                case 403 -> "LLM_FORBIDDEN";
                case 429 -> "LLM_RATE_LIMITED";
                case 500, 502, 503, 504 -> "LLM_PROVIDER_SERVER_ERROR";
                case -1 -> "LLM_PROVIDER_NETWORK_ERROR";
                default -> "LLM_UNKNOWN_ERROR";
            };
        }

        return "LLM_STREAM_ERROR";
    }

    private String toSafeMessage(Throwable ex) {
        if (ex instanceof AllProvidersFailedException) {
            return "所有模型服务暂时不可用，请稍后重试。";
        }

        if (ex instanceof LlmProviderException providerException) {
            return switch (providerException.statusCode()) {
                case 400 -> "模型请求参数错误，请检查 model、messages、max_tokens 等字段。";
                case 401 -> "模型服务认证失败，请检查 API Key。";
                case 403 -> "没有权限访问该模型或资源。";
                case 429 -> "模型服务限流或额度不足，请稍后重试。";
                case 500, 502, 503, 504, -1 -> "模型服务暂时不可用，请稍后重试。";
                default -> "模型服务调用失败。";
            };
        }

        return "模型流式输出失败。";
    }
}
```

## 测试请求

```bash
curl -N \
  -X POST "http://localhost:8080/api/llm/chat/stream" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "system": "你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。",
    "messages": [
      {
        "role": "USER",
        "content": "用三句话解释什么是 RAG。"
      }
    ],
    "options": {
      "temperature": 0.2,
      "maxTokens": 500,
      "topP": null
    },
    "metadata": {}
  }'
```
