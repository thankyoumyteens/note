# ChatClient 简介

`ChatClient` 是 Spring AI 提供的高层聊天客户端。

你可以把它理解成 Spring AI 版的 WebClient，但它不是用来直接发 HTTP 请求的，而是用来和大模型进行聊天交互。

## 它在 Spring AI 里的位置

```text
                    ┌──────────────┐
                    │  Controller  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  ChatClient  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  ChatModel   │
                    └──────┬───────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
      OpenAiChatModel AnthropicChatModel  ...
             │             │
             ▼             ▼
        OpenAI/Qwen     Claude API
```

简单说：

- ChatClient = 业务代码调用大模型的高层入口
- ChatModel = Spring AI 对具体模型的抽象
- OpenAiChatModel / AnthropicChatModel = 具体 provider 的模型实现
- WebClient / RestClient = 底层真正发 HTTP 请求的工具

## 最简单用法

```java
@Service
public class AiChatService {

    private final ChatClient chatClient;

    public AiChatService(ChatClient.Builder builder) {
        this.chatClient = builder
                .defaultSystem("你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。")
                .build();
    }

    public String chat(String message) {
        return chatClient.prompt()
                .user(message)
                .call()
                .content();
    }
}
```

这段代码的含义是：

```text
prompt()  → 开始构造一次模型请求
user()    → 添加 user message
call()    → 发起同步调用
content() → 取出模型返回文本
```

## ChatClient 和 WebClient 的区别

| 对象         | 作用                     | 关注点                                              |
| ------------ | ------------------------ | --------------------------------------------------- |
| `WebClient`  | 通用 HTTP 客户端         | URL、Header、JSON、HTTP status、body                |
| `ChatModel`  | 大模型抽象               | 调哪个模型、模型参数、provider 实现                 |
| `ChatClient` | 面向业务的大模型聊天 API | prompt、system、user、advisor、memory、tool、stream |

例如你手写 WebClient 调 Qwen Anthropic-compatible：

```java
webClient.post()
        .uri("/messages")
        .bodyValue(request)
        .retrieve()
        .bodyToMono(ClaudeMessageResponse.class)
        .block();
```

你要自己处理：

- URL
- headers
- request body
- response body
- 错误状态码
- 字段名
- DTO

而用 ChatClient：

```java
chatClient.prompt()
        .system("你是一个助手")
        .user("解释一下 RAG")
        .call()
        .content();
```

你只需要关心：

- system prompt
- user message
- 模型返回内容

底层 HTTP 细节由 `ChatModel` 和 provider 实现处理。

## ChatClient 和 ChatModel 的区别

可以这么理解：

- ChatModel 更底层
- ChatClient 更面向业务

### ChatModel

偏底层模型调用：

```java
ChatResponse response = chatModel.call(prompt);
```

你需要自己构造 `Prompt`、`Message`、`Options` 等对象。

### ChatClient

偏高层 fluent API：

```java
String content = chatClient.prompt()
        .system("你是 Java 后端助手")
        .user("解释一下 WebClient")
        .call()
        .content();
```

更接近你平时写业务代码的方式。

所以一般项目里：

1. Controller / Service 层优先用 ChatClient
2. 底层框架封装或特殊调用时才直接用 ChatModel

## 为什么要有 ChatClient

如果没有 `ChatClient`，你每接一个模型都要自己写：

```text
OpenAI 请求 DTO
Claude 请求 DTO
Qwen 请求 DTO
DeepSeek 请求 DTO
响应 DTO
错误处理
streaming 解析
tool calling 解析
```

有了 `ChatClient`，你的业务代码可以尽量统一成：

```java
chatClient.prompt()
        .system(systemPrompt)
        .user(userMessage)
        .call()
        .content();
```

它的价值是：

- 统一大模型调用方式
- 减少 provider 差异暴露到业务层
- 让 Spring Boot 项目更像普通业务开发
- 方便接入 memory / advisor / tool calling

这也是 Spring AI 的核心目标之一：把 AI 应用开发带入 Spring 的抽象和模块化体系。
