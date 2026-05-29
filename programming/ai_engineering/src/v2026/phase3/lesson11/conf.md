# 配置数据库和 embedding

给 Java 服务配置 PostgreSQL 连接，以及 embedding 模型参数。

RAG 需要两类模型调用：

```text
chat model：负责最终回答
embedding model：负责把文本变成向量
```

它们是不同能力，不要混在同一个方法里。

#### 代码

修改 `applicationyml`:

```yaml
spring:
  # 把 H2 配置删掉，统一改成 PostgreSQL
  datasource:
    url: jdbc:postgresql://localhost:5432/ai_gateway
    username: ai
    password: ai123456
    driver-class-name: org.postgresql.Driver
  sql:
    init:
      mode: always
      schema-locations: classpath:schema.sql

ai:
  embedding:
    base-url: ${AI_EMBEDDING_BASE_URL:${llm.base-url}}
    api-key: ${AI_EMBEDDING_API_KEY:${llm.api-key}}
    model: ${AI_EMBEDDING_MODEL:BAAI/bge-large-zh-v1.5}
    dimension: ${AI_EMBEDDING_DIMENSION:1024}
```

#### 代码说明

这里允许 embedding 复用 LLM 的 `base-url` 和 `api-key`，但模型名单独配置。

如果你的供应商 embedding 维度不是 `1024`，要同时修改：

```text
ai.embedding.dimension
数据库 vector 维度
```

⚠️ 注意：pgvector 对 vector 的 HNSW / IVFFlat 索引限制在最多 2000 维。
