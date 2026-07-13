# Python 实现客户端断流

FastAPI 返回 `AsyncIterator` 时，客户端关闭页面、刷新页面或主动 abort，当前异步响应任务会被取消，`event_generator()` 会收到 `asyncio.CancelledError`。

修改 `sse_main.py` 中的 `stream_chat()`：

```py
@app.post("/api/llm/chat/stream")
async def stream_chat(request: UnifiedChatRequest) -> StreamingResponse:
    """异步流式聊天接口。"""

    async def event_generator() -> AsyncIterator[str]:
        completed_normally = False  # stream 是否正常结束。

        try:
            async for event in router.stream(request):
                if event.type == StreamEventType.DONE:
                    # 收到 DONE 表示业务流已经正常收尾。
                    completed_normally = True

                yield sse_event(event)

        except asyncio.CancelledError:
            if not completed_normally:
                print(
                    "客户端断开了, requestId="
                    + str(request.metadata.get("requestId"))
                )
                # 这里记录 cancelled 状态，不要按系统异常告警。

            # 继续抛出取消信号，让 Router 和 ProviderClient 关闭上游 stream。
            raise

        except AllProvidersFailedException:
            yield sse_event(
                UnifiedChatStreamEvent(
                    type=StreamEventType.ERROR,
                    error_code="ALL_PROVIDERS_FAILED",
                    error_message="All providers failed",
                )
            )
            completed_normally = True
            yield sse_event(UnifiedChatStreamEvent(type=StreamEventType.DONE))

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
```

这里的 `asyncio.CancelledError` 对应 Reactor 中的 `SignalType.CANCEL`。

`CancelledError` 不继承 `Exception`，所以不会被 Router 中处理 Provider 失败的 `except Exception` 捕获，也不会触发 retry 或 fallback。`raise` 会继续传播取消信号；传播过程中，Router 的 `aclosing` 和 ProviderClient 的 `async with stream` 会依次关闭异步生成器和 SDK HTTP stream。

```text
客户端断开
    → event_generator 收到 CancelledError
    → Router 的 AsyncIterator 被取消
    → ProviderClient 的 AsyncIterator 被取消
    → async with 关闭 SDK stream
    → 上游 HTTP 连接释放
```

客户端取消不是 Provider 调用失败，不要发送 `error` 事件，也不要按系统异常告警。

## 测试

发起一个耗时较长的请求，并让 curl 在三秒后主动断开：

```sh
curl -N \
  --max-time 3 \
  -X POST "http://localhost:8000/api/llm/chat/stream" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "system": "你是一个详细回答问题的 AI 助手。",
    "messages": [
      {
        "role": "user",
        "content": "请从第一章开始写一篇至少五千字的人工智能发展史，每一章都给出详细例子。"
      }
    ],
    "options": {
      "temperature": 0.2,
      "max_tokens": 4000,
      "top_p": null
    },
    "metadata": {
      "requestId": "cutoff-test-001"
    }
  }'
```

正常情况下，curl 会先收到部分 SSE 内容，然后输出类似信息：

```text
curl: (28) Operation timed out after 3000 milliseconds
```

服务端应该输出：

```text
客户端断开了, requestId=cutoff-test-001
```

curl 的退出码 28 是本次测试的预期结果，表示测试客户端主动结束请求，不是服务端异常。
