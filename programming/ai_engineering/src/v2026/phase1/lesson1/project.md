# 环境和项目骨架

今天你先完成环境和项目骨架。

## 你需要准备

建议环境：

```text
JDK 21
Spring Boot 3.x
Maven 或 Gradle
IntelliJ IDEA
Postman / Apifox
一个可用的大模型 API Key
```

如果你还没有 API Key，可以先用任意一个兼容 OpenAI API 格式的平台。

---

## 项目结构建议

创建项目：

```text
ai-gateway
```

包结构：

```text
com.example.aigateway
  ├── controller
  │     └── AiChatController.java
  ├── service
  │     └── AiChatService.java
  ├── client
  │     └── LlmClient.java
  ├── client.openai
  │     └── OpenAiLlmClient.java
  ├── dto
  │     ├── ChatRequest.java
  │     └── ChatResponse.java
  ├── config
  │     └── LlmProperties.java
  └── AiGatewayApplication.java
```

先不要一上来就用 LangChain、LangGraph、RAG。

第一步只做清楚：

```text
Controller -> Service -> LlmClient -> Model API
```
