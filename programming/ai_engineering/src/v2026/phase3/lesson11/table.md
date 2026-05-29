# 创建数据库表

创建文档表和 chunk 表。

RAG 通常不是直接存整篇文档向量，而是存 chunk 向量。

原因：

```text
整篇文档太长，不适合直接塞给模型
用户问题通常只命中文档中的一小部分
chunk 更容易被精确检索
```

#### 代码

创建文件：

```text
src/main/resources/schema-rag.sql
```

内容：

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS rag_documents (
    id UUID PRIMARY KEY,
    filename TEXT NOT NULL,
    content_type TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS rag_chunks (
    id UUID PRIMARY KEY,
    document_id UUID NOT NULL REFERENCES rag_documents(id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1024) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS rag_chunks_embedding_hnsw_idx
ON rag_chunks
USING hnsw (embedding vector_cosine_ops);
```

#### 代码说明

`embedding vector(1024)` 表示向量维度是 1024。

`hnsw` 索引用于加速相似度检索。
