# 重试和降级

整个 Provider 调用链使用异步实现：

```text
FastAPI async endpoint
    → async ProviderFallbackRouter
    → AsyncOpenAI / AsyncAnthropic
    → 异步 HTTP 请求
```

ProviderClient 使用异步 SDK，Router 通过 `await` 依次调用 provider。请求等待模型响应或等待重试间隔时不会阻塞 FastAPI 事件循环。

Tenacity 的 `@retry` 会识别异步 `chat()`，重试退避期间使用异步等待。`asyncio.CancelledError` 不继承 `Exception`，因此任务取消不会被 Router 当成 Provider 失败，也不会触发 retry 或 fallback。

项目结构

```
agent-dev-py
├── .env
├── pyproject.toml
└── src
    └── llm_api_demo
        ├── __init__.py
        ├── settings.py
        ├── schemas.py
        ├── exceptions.py
        ├── provider_clients.py
        ├── fallback_router.py
        └── main.py          # FastAPI 入口
```
