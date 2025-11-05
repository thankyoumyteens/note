# HTTP Client

Java 11 将 Java 9 中引入的 HttpClient API 从孵化阶段正式标准化（位于 java.net.http 包下），替代了老旧的 HttpURLConnection，提供了一套支持同步、异步请求以及 WebSocket 的现代 HTTP 客户端 API。该 API 设计简洁、功能全面，支持 HTTP/1.1 和 HTTP/2，解决了传统 HTTP 客户端的性能和易用性问题。

相比传统的 HttpURLConnection 和第三方库（如 Apache HttpClient），Java 11 标准化的 HttpClient 具有以下优势：

- 支持同步和异步请求：同步请求阻塞当前线程，异步请求基于 CompletableFuture 实现非阻塞，适合高并发场景
- 原生支持 HTTP/2：多路复用、二进制帧等特性，提升多个请求的传输效率（自动协商 HTTP 版本）
- 内置 WebSocket 支持：无需依赖第三方库，可直接建立 WebSocket 连接进行双向通信
- 响应式编程风格：结合 CompletableFuture 和流（Stream）处理响应体，代码更简洁
- 统一的 API 设计：请求构建、拦截器、超时控制等功能模块化，易于扩展和使用
