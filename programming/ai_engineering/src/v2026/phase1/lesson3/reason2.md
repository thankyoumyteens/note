# 什么是 Flux？

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
