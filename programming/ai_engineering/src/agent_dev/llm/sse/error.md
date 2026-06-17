# 错误事件处理

SSE 的错误处理要分两层。

## 1. 建连前错误

例如请求参数错误、鉴权失败、接口不存在。

这类错误发生在 SSE 响应开始之前，可以直接返回普通 HTTP 状态码：

```text
400 Bad Request
401 Unauthorized
403 Forbidden
429 Too Many Requests
500 / 502 / 503
```

这种时候前端不会进入正常 SSE 消息流。

## 2. 建连后错误

一旦已经开始返回 SSE，HTTP 状态码就固定了，通常已经是 200。

后面出错不能再改 HTTP status，只能通过业务事件返回：

```text
event: error
```

错误事件里应该包含：

```text
code
message
retryable
provider
requestId
```

不要把底层异常栈、API Key、provider 原始敏感报错直接返回前端。
