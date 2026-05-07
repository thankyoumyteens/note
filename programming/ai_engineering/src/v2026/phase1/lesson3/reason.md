# 什么是 SSE？

SSE 全称是 Server-Sent Events。

它是一种服务端向客户端持续推送文本事件的 HTTP 技术。

普通 HTTP 响应：

```text
请求一次 -> 响应一次 -> 连接关闭
```

SSE 响应：

```text
请求一次 -> 服务端持续发送事件 -> 最后连接关闭
```

SSE 的响应格式大致是：

```text
data: 第一段内容

data: 第二段内容

data: 第三段内容
```

每个事件之间用空行分隔。

在 Spring Boot 中，可以通过：

```java
MediaType.TEXT_EVENT_STREAM_VALUE
```

声明接口返回 SSE。

---

## SSE 和 WebSocket 的区别

SSE 和 WebSocket 都可以实现“实时效果”，但定位不同。

| 对比项                 | SSE                         | WebSocket                |
| ---------------------- | --------------------------- | ------------------------ |
| 通信方向               | 服务端 -> 客户端单向推送    | 双向通信                 |
| 协议                   | HTTP                        | WebSocket 协议           |
| 实现复杂度             | 低                          | 较高                     |
| 适合场景               | AI 流式回答、日志推送、通知 | 实时协作、游戏、双向聊天 |
| 浏览器支持             | 原生支持 EventSource        | 原生支持 WebSocket       |
| 与大模型流式输出匹配度 | 很高                        | 也可以，但通常没必要     |

AI 聊天中的模型输出，本质上主要是服务端不断向前端推送 token，因此 SSE 通常足够。

---

## 为什么用 `POST + SSE`？

浏览器原生 `EventSource` 默认只支持 GET。

但是 AI 聊天请求通常需要传复杂 JSON body，例如：

```json
{
  "message": "请用五句话解释什么是 RAG"
}
```

所以本课选择：

```http
POST /api/ai/chat/stream
```

并返回：

```http
Content-Type: text/event-stream
```

这在后端和 curl 测试中没有问题。

后续如果做浏览器前端，可以有两种方案：

1. 使用 `fetch + ReadableStream` 读取 POST 流式响应。
2. 改成 GET SSE 接口，把参数放 query string 或通过会话 ID 关联。

当前阶段先用 `POST + SSE`，更贴近实际 AI API 请求方式。
