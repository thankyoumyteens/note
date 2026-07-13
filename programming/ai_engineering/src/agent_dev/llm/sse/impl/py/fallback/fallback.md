# 重试和降级

核心差异：

- 普通 API：失败后可以整体 retry / fallback
- SSE：只有还没输出任何 message chunk 前，才可以 retry / fallback

异步 SSE 还要区分 Provider 异常和任务取消：

- `LlmProviderException`：根据是否已经输出内容决定 retry / fallback
- `asyncio.CancelledError`：表示客户端断开或任务被取消，必须继续抛出，不能进入 retry / fallback

`asyncio.CancelledError` 不继承 `Exception`。因此 Router 使用 `except Exception` 处理 Provider 失败时，不会误吞取消信号；取消会继续传播到 ProviderClient，并由 `async with` 关闭 SDK stream。
