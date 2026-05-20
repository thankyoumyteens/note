# 核心概念

## 什么是 SSE？

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

## 什么是 Flux？

`Flux` 来自 Reactor，是 Spring WebFlux 生态中的响应式流类型。

简单理解：

```java
String
```

表示一个结果。

```java
Flux<String>
```

表示一串结果。

普通聊天接口返回：

```java
ChatResponse
```

意思是：一次性返回完整响应。

流式聊天接口返回：

```java
Flux<String>
```

意思是：不断返回多个字符串片段。

例如：

```java
return Flux.just("hello", "stream", "test");
```

会通过 SSE 输出类似：

```text
data:hello

data:stream

data:test
```
