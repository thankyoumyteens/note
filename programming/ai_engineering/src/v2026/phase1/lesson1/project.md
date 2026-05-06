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

## 为什么需要 `LlmClient` 抽象？

不能让业务代码直接依赖某一个模型供应商。

错误做法：

```text
AiChatService -> OpenAI API
```

更好的做法：

```text
AiChatService -> LlmClient -> OpenAiCompatibleLlmClient
```

`LlmClient` 是一个接口，定义当前系统需要的模型能力。

第一课中它只有一个方法：

```java
public interface LlmClient {

    String chat(String message);
}
```

这样做的好处：

### 1. 隔离模型供应商

以后可以替换为：

```text
OpenAI
Claude
Gemini
DeepSeek
Qwen
公司内部模型网关
```

业务代码不用大改。

### 2. 便于扩展

后续可以继续增加：

```java
String complete(String systemPrompt, String userPrompt);

Flux<String> streamChat(String message);
```

### 3. 便于测试

测试时可以用：

```text
MockLlmClient
```

生产时可以用：

```text
OpenAiCompatibleLlmClient
```

### 4. 便于统一治理

以后所有模型调用都经过 `LlmClient`，就可以统一加：

- 日志
- 统计
- 限流
- 重试
- fallback
- 成本计算
- tracing

## 为什么 Controller 不直接调用模型？

Controller 的职责应该是 HTTP 层处理：

- 接收请求
- 解析 JSON
- 调用 Service
- 返回响应

它不应该关心：

- 用哪个模型
- API Key 是什么
- 如何构造模型请求
- 如何处理模型错误

推荐分层：

```text
Controller：HTTP 入参和出参
Service：业务逻辑
LlmClient：模型能力抽象
具体 Client：模型供应商实现
```

这样可以保持代码职责清晰。
