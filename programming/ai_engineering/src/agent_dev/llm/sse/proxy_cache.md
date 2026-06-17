# 代理缓冲

SSE 要求服务端生成一段，前端就收到一段。但实际链路中间可能有：

```
浏览器
  ↓
Nginx / API Gateway / CDN / Ingress
  ↓
Spring Boot
  ↓
LLM Provider
```

代理默认可能会把响应先缓存起来，等攒够一定大小再发给浏览器。结果就是后端明明在流式输出，前端却很久才收到一大坨内容。

## 需要控制的点

服务端响应必须是：

```
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
```

如果经过 Nginx，还要关闭代理缓冲，例如：

```
proxy buffering off
```

如果是 Nginx，还经常需要返回：

```
X-Accel-Buffering: no
```

如果经过云厂商网关、CDN、负载均衡，也要确认它是否支持长连接流式响应。有些网关会强制缓冲，有些会有固定 idle timeout。
