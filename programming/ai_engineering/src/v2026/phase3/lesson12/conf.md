# 配置 Spring AI VectorStore

让 Spring AI 知道 pgvector 的表、维度、距离类型。

第 11 课你的表是：

```text
rag_documents
rag_chunks
```

Spring AI PgVectorStore 默认表结构和默认表名不一定等于你手写 RAG 的表。官方 API 文档说明，`PgVectorStore` 默认使用 `public.vector_store` 表，并可配置。

为了不破坏第 11 课，本课建议让 Spring AI 使用自己的表：

```text
spring_ai_vector_store
```

#### 代码

在 `application.yml` 中新增 Spring AI vector store 配置。不同 Spring AI 小版本属性名可能略有变化；如果启动时报属性不识别，以当前版本官方配置元数据为准。

建议先加：

```yaml
spring:
  ai:
    vectorstore:
      pgvector:
        initialize-schema: true
        table-name: spring_ai_vector_store
        dimensions: 1024
        distance-type: COSINE_DISTANCE
```

同时保持你已有的 PostgreSQL datasource：

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/ai_gateway
    username: ai
    password: ai123456
    driver-class-name: org.postgresql.Driver
```

#### 代码说明

`dimensions: 1024` 要和你当前 embedding 模型维度保持一致。
