# POST SSE Controller

这是核心：**POST + SSE**。

```java
package com.example.ai.controller;

import com.example.ai.dto.StreamChatRequest;
import com.example.ai.service.LlmStreamRouter;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

/**
 * POST SSE 流式聊天接口。
 * 前端需要使用 fetch + ReadableStream 接收，不使用 EventSource。
 */
@RestController
@RequestMapping("/api/ai")
public class AiStreamController {

    private final LlmStreamRouter router;

    public AiStreamController(LlmStreamRouter router) {
        this.router = router;
    }

    @PostMapping(value = "/chat/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<String>> stream(@RequestBody StreamChatRequest request) {
        Flux<ServerSentEvent<String>> contentEvents = router.stream(request)
                .map(chunk -> ServerSentEvent.builder(chunk)
                        .event("message")
                        .build());

        Flux<ServerSentEvent<String>> doneEvent = Flux.just(
                ServerSentEvent.builder("[DONE]")
                        .event("done")
                        .build()
        );

        return contentEvents
                .onErrorResume(ex -> Flux.just(
                        ServerSentEvent.builder(ex.getMessage())
                                .event("error")
                                .build()
                ))
                .concatWith(doneEvent);
    }
}
```

这里有一个重要点：

- POST SSE 不能用浏览器原生 EventSource。
- EventSource 只适合 GET。
- POST SSE 前端用 fetch + ReadableStream。

## concatWith

作用是：当前面的流结束后，再追加一个 done 事件。

## 正常情况的数据流

前端会收到：

```
event:message
data:RAG

event:message
data: 是一种

event:message
data:检索增强生成

event:done
data:[DONE]
```

## 出错情况的数据流

如果模型输出到一半出错，onErrorResume 会把错误转换成：

```
event:error
data:401 invalid api key
```

然后 concatWith(doneEvent) 继续追加：

```
event:done
data:[DONE]
```

所以最终前端会收到：

```
event:message
data:RAG

event:message
data: 是一种

event:error
data:401 invalid api key

event:done
data:[DONE]
```
