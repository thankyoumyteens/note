# 明确 EmbeddingModel 边界

让 Spring AI Demo 使用 Spring AI 的 `EmbeddingModel`，而不是你第 11 课的 `EmbeddingClient`。

第 11 课：

```text
EmbeddingClient -> OpenAiCompatibleEmbeddingClient
```

第 12 课：

```text
EmbeddingModel -> Spring AI 自动配置的 embedding model
```

Spring AI 的 `EmbeddingModel` 是专门用于生成 embedding 的接口。

#### 代码

如果第 9 课已经配置了 Spring AI OpenAI Starter，确认 `application.yml` 中有类似 Spring AI OpenAI 配置：

```yaml
spring:
  ai:
    openai:
      api-key: ${AI_LLM_API_KEY}
      base-url: ${AI_LLM_BASE_URL}
      embedding:
        options:
          model: BAAI/bge-large-zh-v1.5
```

如果你当前 Spring AI 配置使用的是 chat 模型，也要为 embedding 单独配置模型，避免拿 chat model 去做 embedding。

#### 代码说明

本课 Demo 里可以注入：

```java
private final EmbeddingModel embeddingModel;
```

但很多 Spring AI `VectorStore` 实现会在内部使用已配置的 `EmbeddingModel`。
