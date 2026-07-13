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

## 测试

最简单的测试方法是：发起一个足够长的 SSE 请求，在模型尚未输出完成时主动终止 curl，然后检查服务端是否输出：`客户端断开了, requestId=cutoff-test-001`。

```sh
curl -N \
  --max-time 3 \
  -X POST "http://localhost:8080/api/llm/chat/stream" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "system": "你是一个详细回答问题的 AI 助手。",
    "messages": [
      {
        "role": "USER",
        "content": "请从第一章开始写一篇至少五千字的人工智能发展史，每一章都给出详细例子。"
      }
    ],
    "options": {
      "temperature": 0.2,
      "maxTokens": 4000,
      "topP": null
    },
    "metadata": {
      "requestId": "cutoff-test-001"
    }
  }'
```

`--max-time 3` 表示三秒后由 curl 主动断开连接。正常情况下会看到部分 SSE 内容，然后出现类似提示：

```
curl: (28) Operation timed out after 3000 milliseconds
```

这里的退出码 28 是预期结果，表示测试客户端主动结束了请求，不是服务端异常。
