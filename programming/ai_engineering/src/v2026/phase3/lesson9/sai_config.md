# 配置 Spring AI

在 `application.yml` 增加：

```yaml
spring:
  ai:
    openai:
      api-key: ${OPENAI_API_KEY}
      base-url: https://api.openai.com
      chat:
        options:
          model: gpt-4o-mini
          temperature: 0.1
```

Spring AI OpenAI 文档说明，连接属性使用 `spring.ai.openai` 前缀，chat 选项使用 `spring.ai.openai.chat.options`，例如 model 和 temperature。

如果你使用 OpenAI-compatible 平台，需要根据供应商支持情况调整：

```yaml
spring:
  ai:
    openai:
      api-key: ${OPENAI_API_KEY}
      base-url: 你的兼容平台 base-url
      chat:
        completions-path: /v1/chat/completions
        options:
          model: 你的模型名
          temperature: 0.1
```

## 增加 LLM Provider 配置

在 `application.yml` 增加：

```yaml
llm:
  provider: openai-compatible
```

默认继续使用你的旧实现。

如果要切换到 Spring AI：

```yaml
llm:
  provider: spring-ai
```
