# Spring AI

核心区别是：之前手写 `WebClient` 时，你要自己解析 provider 原始 SSE；用 Spring AI 时，Spring AI 帮你处理 provider streaming，你只需要拿到：

```java
Flux<String>
```

然后 Controller 再包装成你自己的 SSE 协议就行了。
