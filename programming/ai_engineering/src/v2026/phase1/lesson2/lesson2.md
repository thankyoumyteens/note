# 第 2 课：接入真实模型 API

## 本课目标

完成这个调用链：

```text
POST /api/ai/chat
   ↓
AiChatController
   ↓
AiChatService
   ↓
OpenAiCompatibleLlmClient
   ↓
大模型 API
   ↓
返回真实回答
```

本课会加入：

```text
application.yml 配置
WebClient
API Key
超时设置
错误处理
OpenAI-compatible 请求格式
```

Spring 官方文档里，`WebClient` 是 Spring WebFlux 提供的非阻塞 HTTP 客户端，支持 Reactor Netty、JDK HttpClient、Jetty 等底层实现；生产项目里也可以配置连接超时和响应超时。
