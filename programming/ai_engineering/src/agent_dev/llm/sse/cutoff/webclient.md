# WebClient 实现客户端断流

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

doFinally 和 SignalType.CANCEL 是 Reactor 里的概念，也就是 Spring WebFlux / WebClient / Spring AI 流式调用背后的响应式编程机制。

doFinally 就像 Java 里的 finally，doFinally 作用在 Flux / Mono 上。它会在流结束时执行一次。

常见的 SignalType 有这些：

```java
SignalType.ON_COMPLETE // 正常完成
SignalType.ON_ERROR    // 出错结束
SignalType.CANCEL      // 被取消
```

在 SSE 场景里，SignalType.CANCEL 特别重要。比如前端正在接收 stream，这时候用户关闭页面、刷新页面、浏览器调用 `AbortController.abort()`，后端返回给前端的 Flux 就会被取消。Reactor 会给这个流一个结束信号：SignalType.CANCEL。所以你可以这样识别“客户端断开了”。
