# HttpClient

核心类:

- HttpClient：HTTP 客户端实例，负责发送请求，可配置连接超时、代理、SSL 等
- HttpRequest：表示 HTTP 请求，包含 URL、方法（GET/POST 等）、 headers、body 等
- HttpResponse：表示 HTTP 响应，包含状态码、headers、响应体（BodyHandler 处理）
- WebSocket：WebSocket 客户端，支持发送消息和监听事件
