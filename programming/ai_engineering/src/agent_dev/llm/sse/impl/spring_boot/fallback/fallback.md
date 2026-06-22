# 重试和降级

流式输出和普通 JSON 返回不同：

- 非 stream：失败后可以整体重试 / 整体降级
- stream：只有在还没输出任何 token 之前，才允许重试 / 降级。一旦已经输出 token，stream 中途错误，就应该转成 SSE error event 返回给前端
