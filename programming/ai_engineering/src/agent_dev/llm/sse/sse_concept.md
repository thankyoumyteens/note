# 什么是 SSE

SSE 全称：Server-Sent Events。

中文可以理解为：服务器向浏览器持续推送事件。

它的特点是：

1. 基于普通 HTTP
2. 单向通信：server → client
3. 浏览器原生支持 EventSource
4. 很适合模型流式文本输出
5. 比 WebSocket 简单

## Streaming 和 SSE 的关系

这两个词不是完全同一层东西。

```text
Streaming
= 一种响应方式
= 数据分块返回

SSE
= 一种 HTTP 传输格式
= 用 event/data/id/retry 这种格式推送事件
```

在大模型 API 里，经常是：

1. 模型 API 使用 streaming
2. 底层传输格式使用 SSE

## SSE 数据长什么样

SSE 响应不是普通 JSON，而是一行一行的事件流。

典型格式：

```text
event: message
data: {"text":"你"}

event: message
data: {"text":"好"}

event: done
data: [DONE]
```

最常见的是只用 `data:`：

```text
data: {"delta":"你"}

data: {"delta":"好"}

data: [DONE]
```

注意：SSE 每个事件之间通常有一个空行。
