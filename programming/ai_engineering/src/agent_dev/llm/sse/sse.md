# Streaming / SSE 与统一响应协议

Streaming / SSE 流式输出：模型不是等完整答案生成完再一次性返回，而是边生成边返回；后端再把这些小片段继续转发给前端。

这对大模型应用非常重要，因为用户不用等 10 秒、30 秒才看到结果，而是马上看到文字一点点出来。

需要掌握：

- Streaming 与 SSE 的基本概念
- OpenAI-compatible streaming 事件解析
- Anthropic Messages streaming 事件解析
- 使用 Java 和 Python 实现 SSE
- 前端 fetch + ReadableStream 接收 POST SSE
- 后端统一封装前端事件协议
- message / error / done 事件设计
- 代理缓冲、超时、断流、错误事件处理
