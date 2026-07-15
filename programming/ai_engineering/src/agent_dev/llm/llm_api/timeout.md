# 三类超时

| 类型 | 范围 | 作用 |
| --- | --- | --- |
| 连接超时 | 建立 TCP、TLS 或代理连接 | 防止 Provider 地址不可达时长期等待 |
| 响应超时 | 连接建立后等待或读取响应 | 防止 Provider 长时间没有返回数据 |
| 请求级总超时 | 单次 Provider 尝试的完整调用 | 限制连接、发送请求、等待响应和读取结果的总时间 |

请求级总超时是单次尝试的外层上限，连接超时和响应超时负责更具体的网络阶段；哪个先达到就先终止调用。

## 三种实现

| 实现 | 当前项目的处理方式 |
| --- | --- |
| Spring Boot + WebClient | Reactor Netty 配置连接和响应超时，Reactor `timeout` 限制单次 Provider 尝试的总时间 |
| Spring AI | `CompletableFuture.orTimeout` 限制单次 ChatClient 调用；底层连接和读取超时由具体 ChatModel 使用的 HTTP 客户端配置 |
| Python + uv | 异步 SDK 的 `timeout` 限制单次 Provider 调用；需要更细控制时再使用 SDK 的连接、读取和写入超时配置 |

当前 Spring AI 和 Python 示例只显式暴露请求级总超时，没有把底层连接和响应超时拆成独立配置。

## 与重试和降级的关系

三类超时都属于没有 HTTP 状态码的临时错误，统一使用 `statusCode = -1`：

1. 当前 Provider 超时后先按配置重试。
2. 当前 Provider 重试耗尽后再降级到下一个 Provider。
3. 所有 Provider 都失败后抛出 `AllProvidersFailedException`。

请求级总超时只限制一次尝试，不限制整个重试和降级链；整个调用可能包含多次超时和退避等待。
