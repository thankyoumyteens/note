# 切换到 Spring AI Provider 测试

验证同一套 Controller / Service 可以在不改业务代码的情况下切换底层模型实现。

这就是 `LlmClient` 抽象的价值：

```text
业务层不关心你底层是 WebClient 手写，还是 Spring AI ChatClient。
```

#### 代码

把 `application.yml` 改成：

```yaml
llm:
  provider: spring-ai
```

确认 Spring AI 配置存在：

```yaml
spring:
  ai:
    openai:
      api-key: ${OPENAI_API_KEY}
      base-url: ${OPENAI_BASE_URL:https://api.openai.com}
      chat:
        options:
          model: ${OPENAI_MODEL:gpt-4o-mini}
```

#### 代码说明

现在所有原有接口都应该继续走：

```text
Controller -> Service -> LlmClient
```

只是 `LlmClient` 实现从：

```text
OpenAiCompatibleLlmClient
```

切换为：

```text
SpringAiLlmClient
```
