# OpenAI-compatible Stream Client

这里使用 `bodyToFlux(ServerSentEvent<String>)` 接收 provider 返回的 SSE，再解析 `data`。

```java
package com.example.ai.client;

import com.example.ai.config.AiProviderProperties;
import com.example.ai.dto.LlmMessage;
import com.example.ai.dto.StreamChatRequest;
import com.example.ai.dto.openai.OpenAiChatStreamRequest;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;

import java.util.ArrayList;
import java.util.List;

/**
 * OpenAI-compatible streaming client。
 * 支持 OpenAI / Qwen / DeepSeek 的 /chat/completions streaming。
 */
@Component
public class OpenAiCompatibleStreamClient implements ProviderStreamClient {

    private static final ParameterizedTypeReference<ServerSentEvent<String>> SSE_STRING =
            new ParameterizedTypeReference<>() {
            };

    private final WebClient.Builder webClientBuilder;
    private final ObjectMapper objectMapper;

    public OpenAiCompatibleStreamClient(WebClient.Builder webClientBuilder,
                                        ObjectMapper objectMapper) {
        this.webClientBuilder = webClientBuilder;
        this.objectMapper = objectMapper;
    }

    @Override
    public boolean supports(AiProviderProperties.ProviderType type) {
        return type == AiProviderProperties.ProviderType.OPENAI_CHAT_COMPLETIONS;
    }

    @Override
    public Flux<String> stream(AiProviderProperties.ProviderConfig config,
                               StreamChatRequest request) {
        WebClient webClient = webClientBuilder
                .baseUrl(config.baseUrl())
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + config.apiKey())
                .build();

        OpenAiChatStreamRequest body = new OpenAiChatStreamRequest(
                config.model(),
                buildMessages(request),
                config.temperature(),
                config.maxTokens(),
                true
        );

        return webClient.post()
                .uri(config.path())
                .bodyValue(body)
                .retrieve()
                .onStatus(
                        HttpStatusCode::isError,
                        response -> response.bodyToMono(String.class)
                                .map(errorBody -> new RuntimeException(
                                        "OpenAI-compatible streaming error, status="
                                                + response.statusCode()
                                                + ", body="
                                                + errorBody
                                ))
                )
                .bodyToFlux(SSE_STRING)
                .map(ServerSentEvent::data)
                .takeUntil(data -> "[DONE]".equals(data))
                .filter(data -> data != null && !data.isBlank() && !"[DONE]".equals(data))
                .map(this::extractOpenAiDelta)
                .filter(chunk -> !chunk.isBlank());
    }

    private List<LlmMessage> buildMessages(StreamChatRequest request) {
        List<LlmMessage> messages = new ArrayList<>();

        if (request.system() != null && !request.system().isBlank()) {
            messages.add(new LlmMessage("system", request.system()));
        }

        messages.add(new LlmMessage("user", request.message()));
        return messages;
    }

    private String extractOpenAiDelta(String data) {
        try {
            JsonNode root = objectMapper.readTree(data);
            return root.path("choices")
                    .path(0)
                    .path("delta")
                    .path("content")
                    .asText("");
        } catch (Exception e) {
            return "";
        }
    }
}
```

OpenAI / DeepSeek 这类 OpenAI-compatible streaming 返回给后端的原始流可能是：

```json
data: {"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"role":"assistant"},"finish_reason":null}]}

data: {"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"RAG"},"finish_reason":null}]}

data: {"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":" 是一种"},"finish_reason":null}]}

data: {"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"检索增强生成"},"finish_reason":null}]}

data: {"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"技术"},"finish_reason":null}]}

data: {"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

## bodyToFlux(SSE_STRING)

由于：

```java
private static final ParameterizedTypeReference<ServerSentEvent<String>> SSE_STRING =
        new ParameterizedTypeReference<>() {
        };
```

那么 `.bodyToFlux(SSE_STRING)` 会把原始 SSE 流解析成：`Flux<ServerSentEvent<String>>`。

逻辑上类似这样：

```java
ServerSentEvent(
  event = null,
  data = "{\"id\":\"chatcmpl-001\",\"object\":\"chat.completion.chunk\",\"choices\":[{\"index\":0,\"delta\":{\"role\":\"assistant\"},\"finish_reason\":null}]}"
)

ServerSentEvent(
  event = null,
  data = "{\"id\":\"chatcmpl-001\",\"object\":\"chat.completion.chunk\",\"choices\":[{\"index\":0,\"delta\":{\"content\":\"RAG\"},\"finish_reason\":null}]}"
)

ServerSentEvent(
  event = null,
  data = "{\"id\":\"chatcmpl-001\",\"object\":\"chat.completion.chunk\",\"choices\":[{\"index\":0,\"delta\":{\"content\":\" 是一种\"},\"finish_reason\":null}]}"
)

ServerSentEvent(
  event = null,
  data = "{\"id\":\"chatcmpl-001\",\"object\":\"chat.completion.chunk\",\"choices\":[{\"index\":0,\"delta\":{\"content\":\"检索增强生成\"},\"finish_reason\":null}]}"
)

ServerSentEvent(
  event = null,
  data = "{\"id\":\"chatcmpl-001\",\"object\":\"chat.completion.chunk\",\"choices\":[{\"index\":0,\"delta\":{\"content\":\"技术\"},\"finish_reason\":null}]}"
)

ServerSentEvent(
  event = null,
  data = "{\"id\":\"chatcmpl-001\",\"object\":\"chat.completion.chunk\",\"choices\":[{\"index\":0,\"delta\":{},\"finish_reason\":\"stop\"}]}"
)

ServerSentEvent(
  event = null,
  data = "[DONE]"
)
```

## map(ServerSentEvent::data)

作用是从每个 SSE 事件中取出 data。

处理后数据变成：

```json
{"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"role":"assistant"},"finish_reason":null}]}

{"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"RAG"},"finish_reason":null}]}

{"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":" 是一种"},"finish_reason":null}]}

{"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"检索增强生成"},"finish_reason":null}]}

{"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"技术"},"finish_reason":null}]}

{"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

[DONE]
```

此时的 String 还不是最终文本，而是 provider 返回的 JSON chunk。

## takeUntil

作用是：一直读取 data，直到遇到 `[DONE]` 为止。

注意：takeUntil 会保留触发条件的元素。也就是说，经过这一步后，`[DONE]` 仍然在流里。

由于设定 ProviderStreamClient 只返回文本片段，Controller 统一发送前端协议里的 done 事件。所以后面还需要把原始的 `[DONE]` 过滤掉。

## `filter(data -> data != null && !data.isBlank() && !"[DONE]".equals(data))`

作用是过滤掉：

- null
- 空字符串
- 空白字符串
- `[DONE]`

经过这一步后，数据变成：

```json
{"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"role":"assistant"},"finish_reason":null}]}

{"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"RAG"},"finish_reason":null}]}

{"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":" 是一种"},"finish_reason":null}]}

{"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"检索增强生成"},"finish_reason":null}]}

{"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"技术"},"finish_reason":null}]}

{"id":"chatcmpl-001","object":"chat.completion.chunk","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}
```

此时 `[DONE]` 已经被移除了。

## map(this::extractOpenAiDelta)

作用是从每个 JSON chunk 里提取：`choices[0].delta.content`。

经过这一步后，数据变成：

```java
""
"RAG"
" 是一种"
"检索增强生成"
"技术"
""
```

## filter(chunk -> !chunk.isBlank())

作用是过滤掉解析后的空文本。

经过这一步后，数据最终变成：

```
RAG
 是一种
检索增强生成
技术
```

## 如果前端想要 JSON data 格式

如果前端需要返回特定格式的数据，可以在最后的 filter 后面追加 map 进行处理：

```java
.filter(chunk -> !chunk.isBlank())
.map(text -> "{\"content\": \"" + text + "\"}");
```

这样，数据最终变成：

```json
{"content": "RAG"}
{"content": " 是一种"}
{"content": "检索增强生成"}
{"content": "技术"}
```
