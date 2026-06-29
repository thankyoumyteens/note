# Reactor 简介

## Reactor 是什么

Reactor 是 Spring WebFlux 底层使用的响应式编程库。

可以简单理解为：Reactor = Java 里的异步流处理框架。

它最核心的两个类型是：

```text
Mono<T> = 未来产生 0 或 1 个结果
Flux<T> = 未来产生 0 到 N 个结果
```

在 LLM 调用场景里：

1. 非 stream 调用：
   - 一次请求，最终返回一个完整结果
   - 适合用 `Mono<UnifiedChatResponse>`
2. stream 调用：
   - 一次请求，持续返回多个 chunk
   - 适合用 `Flux<UnifiedChatStreamEvent>`

## 为什么 WebClient Stream 会用到 Flux

LLM stream 不是一次性返回完整文本，而是一段一段返回：

```text
chunk1
chunk2
chunk3
...
[DONE]
```

所以 WebClient 会把上游 SSE 流表示成：`Flux<ServerSentEvent<String>>`，后续可以再把它转换成自定义的业务事件：`Flux<MyStreamEvent>`。

完整链路是：

```text
上游 LLM SSE chunk
        ↓
Flux<ServerSentEvent<String>>
        ↓
Flux<MyStreamEvent>
        ↓
Flux<ServerSentEvent<MyStreamEventResponse>>
        ↓
前端
```

## subscribe 是什么

subscribe 是 Reactor 流真正开始执行的开关。

可以这样理解：

```text
Flux / Mono = 定义如何执行计划
subscribe = 开始执行计划
```

例如：

```text
创建 Flux
  ↓
只是描述“将来要做什么”
  ↓
还没有真正执行
  ↓
发生 subscribe
  ↓
真正发起 HTTP 请求
  ↓
开始接收 stream chunk
```

在 Spring WebFlux Controller 里，一般不需要手动写 `subscribe()`：

```text
Controller 返回 Flux
        ↓
Spring 框架负责 subscribe
        ↓
WebClient 请求真正发出
        ↓
SSE 数据持续写回前端
```

所以原则是：

1. 业务代码不要随便手动 subscribe
2. Controller 直接 return Mono / Flux
3. 让 Spring 管理订阅、错误、取消和响应输出

错误示例：

```java
router.stream(request).subscribe();
return "ok";
```

问题是：

- 异步流程脱离 Spring 管理
- 错误不好处理
- 请求取消不好感知
- SSE 无法正常回写
- 链路追踪也容易断
