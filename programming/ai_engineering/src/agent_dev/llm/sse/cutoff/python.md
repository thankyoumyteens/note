# Python 实现客户端断流

Python 同步生成器被关闭时会收到 `GeneratorExit`。

为了可靠释放上游连接，需要分别处理三件事：

1. sse_main.py: 用 GeneratorExit 识别客户端断开，结束生成器。
2. stream_fallback_router.py: 关闭当前 provider_stream，把关闭动作向下传播。
3. stream_provider_clients.py: 在 finally 中关闭 OpenAI或 Anthropic SDK stream，真正释放 HTTP 连接。

修改 stream_provider_clients.py：

```py
# 这里以 OpenAiCompatibleStreamProviderClient._stream_once() 为例，
# AnthropicStreamProviderClient.stream() 也要使用相同方式关闭 SDK stream。
# 在原方法中增加 stream = None 和 finally
def _stream_once(self, request: UnifiedChatRequest) -> Iterator[UnifiedChatStreamEvent]:
    """执行一次 OpenAI-compatible streaming 请求。"""
    stream = None  # 当前 OpenAI-compatible SDK stream。

    try:
        messages = [{"role": "system", "content": request.system}]

        for message in request.messages:
            messages.append({"role": message.role.value, "content": message.content})

        stream = self.client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=request.options.temperature,
            max_tokens=request.options.max_tokens,
            top_p=request.options.top_p,
            stream=True,
        )

        for chunk in stream:
            if not chunk.choices:
                continue

            content = chunk.choices[0].delta.content

            if content:
                yield UnifiedChatStreamEvent(
                    type=StreamEventType.MESSAGE,
                    provider=self._provider,
                    model=chunk.model or self._model,
                    content=content,
                )

    except (APITimeoutError, APIConnectionError) as exc:
        raise LlmProviderException(self.provider, -1, f"{self.provider} timeout or connection error") from exc
    except APIError as exc:
        raise LlmProviderException(
            self.provider,
            getattr(exc, "status_code", -1) or -1,
            str(exc),
            str(getattr(exc, "response", "")),
        ) from exc
    finally:
        if stream is not None:
            # Router 关闭当前 Provider 生成器时，继续关闭上游 HTTP stream。
            stream.close()
```

修改 stream_fallback_router.py：

```py
# 把 client.stream(request) 保存为当前 Provider 生成器，并在 finally 中关闭
def stream(self, request: UnifiedChatRequest) -> Iterator[UnifiedChatStreamEvent]:
    """只有当前 provider 尚未输出 message chunk 时，才允许 fallback。"""
    failures: list[LlmProviderException] = []

    for client in self.clients:
        content_started = False
        provider_stream = client.stream(request)  # 当前 provider 流式生成器。

        try:
            for event in provider_stream:
                if event.type == StreamEventType.MESSAGE:
                    content_started = True

                yield event

            yield UnifiedChatStreamEvent(type=StreamEventType.DONE)
            return

        except Exception as exc:
            provider_exception = self._to_provider_exception(client.provider, exc)
            failures.append(provider_exception)

            if content_started:
                yield UnifiedChatStreamEvent(
                    type=StreamEventType.ERROR,
                    error_code="STREAM_INTERRUPTED",
                    error_message=provider_exception.message,
                )
                yield UnifiedChatStreamEvent(type=StreamEventType.DONE)
                return

            if not self._should_fallback(provider_exception):
                yield UnifiedChatStreamEvent(
                    type=StreamEventType.ERROR,
                    error_code="PROVIDER_FAILED",
                    error_message=provider_exception.message,
                )
                yield UnifiedChatStreamEvent(type=StreamEventType.DONE)
                return
        finally:
            # event_generator 被关闭时，把关闭动作继续传给 ProviderClient。
            provider_stream.close()

    raise AllProvidersFailedException(failures)
```

最后修改 sse_main.py：

```py
@app.post("/api/llm/chat/stream")
def stream_chat(request: UnifiedChatRequest) -> StreamingResponse:

    def event_generator() -> Iterator[str]:
        completed_normally = False  # stream 是否正常结束。

        try:
            for event in router.stream(request):
                if event.type == StreamEventType.DONE:
                    # 收到 DONE 表示业务流已经正常收尾。
                    completed_normally = True

                yield sse_event(event)

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

        # 处理客户端断流
        except GeneratorExit:
            if not completed_normally:
                print(
                    "客户端断开了, requestId="
                    + str(request.metadata.get("requestId"))
                )
                # 这里记录 cancelled 状态，不要按系统异常告警。

            # 重新抛出刚捕获的 GeneratorExit，让 Router 和 ProviderClient 执行关闭逻辑。
            raise

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

这里的 `GeneratorExit` 对应 Reactor 中的 `SignalType.CANCEL`，生成器中的 `finally` 对应 `doFinally`。

## 测试

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
      "maxTokens": 4000,
      "topP": null
    },
    "metadata": {
      "requestId": "cutoff-test-001"
    }
  }'
```
