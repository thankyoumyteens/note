# 添加 Spring AI PgVector 依赖

让 Spring AI 自动提供 `VectorStore`，用来连接 PostgreSQL + pgvector。

第 11 课你自己写了：

```text
RagChunkRepository
RagDocumentRepository
ORDER BY embedding <=> ?::vector
```

Spring AI 的 `VectorStore` 把这些读写和相似度搜索封装起来。

#### 代码

在 `pom.xml` 增加依赖。Spring AI 1.1.x 的 artifact 名称可能因 BOM 管理而有所不同，优先使用你项目当前 BOM 能解析的名称。

先尝试：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-vector-store-pgvector</artifactId>
</dependency>
```

如果 Maven 提示找不到，再换成：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-pgvector-store</artifactId>
</dependency>
```

这里不要删除第 11 课的手写 RAG 类。Spring AI RAG 是并行 Demo。
