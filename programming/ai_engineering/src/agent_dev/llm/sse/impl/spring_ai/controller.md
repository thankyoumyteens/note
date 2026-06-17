# POST SSE Controller

这是后端对前端暴露的 POST SSE 接口。

```java
package com.example.ai.controller;

import com.example.ai.dto.StreamChatRequest;
import com.example.ai.service.SpringAiStreamRouter;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

/**
 * Spring AI POST SSE Controller。
 * 前端使用 fetch + ReadableStream 接收，不使用 EventSource。
 */
@RestController
@RequestMapping("/api/ai")
public class SpringAiStreamController {

    private final SpringAiStreamRouter router;

    public SpringAiStreamController(SpringAiStreamRouter router) {
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
                        ServerSentEvent.builder(toSafeErrorMessage(ex))
                                .event("error")
                                .build()
                ))
                .concatWith(doneEvent);
    }

    private String toSafeErrorMessage(Throwable ex) {
        if (ex.getMessage() == null || ex.getMessage().isBlank()) {
            return "AI streaming failed";
        }

        return ex.getMessage();
    }
}
```

前端最终收到的不是 provider 原始 SSE，而是你自己的统一 SSE 协议：

```text
event:message
data:文本片段

event:error
data:错误信息

event:done
data:[DONE]
```
