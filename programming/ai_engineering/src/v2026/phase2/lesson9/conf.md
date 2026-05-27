# 配置 Spring AI OpenAI 参数

让 Spring AI 知道要调用哪个模型、使用哪个 API Key。

你之前的手写 Client 使用的是自定义配置：

```yaml
llm:
  base-url:
  api-key:
  model:
```

Spring AI 使用自己的配置前缀：

```yaml
spring:
  ai:
    openai:
      api-key:
      base-url:
      chat:
        options:
          model:
```

Spring AI 项目页的 getting started 示例也展示了通过 `spring.ai.openai.api-key` 配置 OpenAI key，并通过 `ChatClient.Builder` 创建 ChatClient 调用模型。

#### 代码

修改 `application.yml`：

```yaml
llm:
  provider: openai-compatible

spring:
  ai:
    openai:
      api-key: ${OPENAI_API_KEY}
      base-url: ${OPENAI_BASE_URL:https://api.openai.com}
      chat:
        options:
          model: ${OPENAI_MODEL:gpt-4o-mini}
```

如果你使用的是 OpenAI-compatible 第三方供应商，把：

```text
OPENAI_BASE_URL
OPENAI_API_KEY
OPENAI_MODEL
```

改成对应值。

#### 代码说明

`llm.provider` 是我们自己的切换开关。

```yaml
llm:
  provider: openai-compatible
```

表示继续使用你手写的 `OpenAiCompatibleLlmClient`。

```yaml
llm:
  provider: spring-ai
```

表示切换到本课新增的 `SpringAiLlmClient`。
