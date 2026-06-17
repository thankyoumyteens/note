# 超时处理

SSE 是长连接，所以超时比普通 HTTP 更复杂。

常见超时来源有：

- 浏览器连接超时
- Nginx read timeout
- API Gateway idle timeout
- Spring Boot async timeout
- WebClient 调 provider 超时
- LLM Provider 首 token 超时
- LLM Provider 总生成超时

其中最危险的是 **idle timeout**。

也就是：连接还活着，但一段时间没有任何数据流过，中间代理认为连接空闲，就把它断了。

## 心跳机制

SSE 最好定期发送 heartbeat。

心跳不是业务内容，只是告诉代理和浏览器：这个连接还活着，不要断开。

常见间隔：

- 15 秒
- 20 秒
- 30 秒

不要太短，否则浪费连接资源；不要太长，否则可能超过网关 idle timeout。

## 超时分类

工程上建议分三类：

### 1. 首 token 超时

模型迟迟没有开始输出。

说明可能是：

- provider 排队
- 请求上下文过长
- 模型响应慢
- 网络异常

处理方式：

- 给前端发送 error 事件
- 结束 SSE
- 记录 provider latency
- 必要时 fallback 到其他 provider

### 2. 流中空闲超时

模型中途长时间没输出。

处理方式：

- 发送 heartbeat
- 如果 provider 真断了，再发送 error 事件
- 结束连接

### 3. 总时长超时

整个 SSE 不能无限挂着。

例如限制：单次 SSE 最多 60 秒 / 120 秒 / 300 秒

超时后明确结束，不要让连接永久占资源。
