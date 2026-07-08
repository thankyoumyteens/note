# Spring AI 实现客户端断流

Spring AI 的思路一样。`ChatClient.stream()` 返回的也是响应式流，客户端断开时，Controller 返回的 Flux 也会收到 SignalType.CANCEL。

修改 LlmStreamController：

```java
@PostMapping(value = "/chat/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ServerSentEvent<StreamEventResponse>> stream(
        @RequestBody UnifiedChatRequest request
) {
    // 标识 stream 是否正常结束
    AtomicBoolean completedNormally = new AtomicBoolean(false);

    Flux<ServerSentEvent<StreamEventResponse>> contentEvents = router.stream(request)
            .map(this::toSseEvent);

    Flux<ServerSentEvent<StreamEventResponse>> heartbeatEvents = Flux.interval(Duration.ofSeconds(15))
            .map(tick -> ServerSentEvent.<StreamEventResponse>builder(StreamEventResponse.heartbeat())
                    .event("heartbeat")
                    .build());

    return Flux.merge(contentEvents, heartbeatEvents)
            .takeUntil(sse -> {
                boolean done = "done".equals(sse.event());
                if (done) {
                    // 标记 stream 正常结束
                    completedNormally.set(true);
                }
                return done;
            })
            .onErrorResume(ex -> Flux.just(toErrorEvent(ex), doneEvent()))
            .doFinally(signalType -> {
                if (signalType == SignalType.CANCEL && !completedNormally.get()) {
                    System.out.println("客户端断开了, requestId=" + request.metadata().get("requestId"));
                    // 这里记录 cancelled 状态，不要按系统异常告警
                }
            });
}
```
