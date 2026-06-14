# 修改返回的格式

如果前端想要：

```json
event:message
data: {"content": "检索增强生成"}
```

### 1. 用 DTO 包装 content

定义响应 DTO：

```java
public record StreamMessageEvent(String content) {
}

public record StreamErrorEvent(String message) {
}

public record StreamDoneEvent(boolean done) {
}
```

### 2. 修改 Controller

```java
@PostMapping(value = "/chat/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ServerSentEvent<Object>> stream(@RequestBody StreamChatRequest request) {
    Flux<ServerSentEvent<Object>> contentEvents = router.stream(request)
            .map(chunk -> ServerSentEvent.<Object>builder(new StreamMessageEvent(chunk))
                    .event("message")
                    .build());

    Flux<ServerSentEvent<Object>> doneEvent = Flux.just(
            ServerSentEvent.<Object>builder(new StreamDoneEvent(true))
                    .event("done")
                    .build()
    );

    return contentEvents
            .onErrorResume(ex -> Flux.just(
                    ServerSentEvent.<Object>builder(new StreamErrorEvent(toSafeErrorMessage(ex)))
                            .event("error")
                            .build()
            ))
            .concatWith(doneEvent);
}
```

这样前端收到的会变成类似：

```
event:message
data:{"content":"检索增强生成"}

event:done
data:{"done":true}
```
