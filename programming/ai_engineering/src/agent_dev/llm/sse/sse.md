# Streaming / SSE 流式输出

Streaming / SSE 流式输出：模型不是等完整答案生成完再一次性返回，而是边生成边返回；后端再把这些小片段继续转发给前端。

这对大模型应用非常重要，因为用户不用等 10 秒、30 秒才看到结果，而是马上看到文字一点点出来。

## 什么是 Streaming

普通非流式调用是这样：

1. 用户发问题
2. 后端请求模型 API
3. 模型生成完整答案
4. 一次性返回完整 JSON
5. 前端显示完整答案

缺点：

1. 首屏等待时间长
2. 用户不知道模型是不是卡住了
3. 长答案体验很差

Streaming 是这样：

1. 用户发问题
2. 后端请求模型 API，stream=true
3. 模型生成一个 token / chunk 就返回一个 chunk
4. 后端持续接收 chunk
5. 后端持续推给前端
6. 前端边收边显示

视觉效果就是 ChatGPT 那种：

```text
这
这 是 一
这 是 一个 流 式
...
```

## 什么是 SSE

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
