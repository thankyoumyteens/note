# 修改数据库表，加入权限字段

让文档和 chunk 都携带权限元数据。RAG 权限过滤不能只放在 Java 内存里，必须进入数据库查询条件。

权限隔离 RAG 的关键是：

```text
检索前过滤，而不是检索后过滤。
```

如果先从全库检索 top-k，再在 Java 里过滤，可能出现两个问题：

```text
1. top-k 中全是无权限 chunk，过滤后没有结果
2. 越权数据已经被检索层读出来，存在泄露风险
```

所以权限条件必须写进 SQL。

#### 代码

修改 `schema.sql` 中的 RAG 表。

如果你是开发环境，可以直接 drop 重建；如果已有数据，需要写 migration。当前课程项目先用开发方式。

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS rag_documents (
    id UUID PRIMARY KEY,
    filename TEXT NOT NULL,
    content_type TEXT,

    tenant_id TEXT NOT NULL,
    owner_user_id TEXT NOT NULL,
    visibility TEXT NOT NULL,
    allowed_roles TEXT[] NOT NULL DEFAULT '{}',
    allowed_users TEXT[] NOT NULL DEFAULT '{}',

    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS rag_chunks (
    id UUID PRIMARY KEY,
    document_id UUID NOT NULL REFERENCES rag_documents(id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1024) NOT NULL,

    tenant_id TEXT NOT NULL,
    owner_user_id TEXT NOT NULL,
    visibility TEXT NOT NULL,
    allowed_roles TEXT[] NOT NULL DEFAULT '{}',
    allowed_users TEXT[] NOT NULL DEFAULT '{}',

    created_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS rag_chunks_embedding_hnsw_idx
ON rag_chunks
USING hnsw (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS rag_chunks_tenant_id_idx
ON rag_chunks (tenant_id);

CREATE INDEX IF NOT EXISTS rag_chunks_owner_user_id_idx
ON rag_chunks (owner_user_id);

CREATE INDEX IF NOT EXISTS rag_chunks_visibility_idx
ON rag_chunks (visibility);

CREATE INDEX IF NOT EXISTS rag_chunks_allowed_roles_gin_idx
ON rag_chunks
USING gin (allowed_roles);

CREATE INDEX IF NOT EXISTS rag_chunks_allowed_users_gin_idx
ON rag_chunks
USING gin (allowed_users);
```

开发阶段重建表：

```bash
docker exec -it ai-gateway-pgvector psql -U ai -d ai_gateway
```

执行：

```sql
DROP TABLE IF EXISTS rag_chunks;
DROP TABLE IF EXISTS rag_documents;
```

#### 代码说明

这里把权限字段同时放到 `rag_documents` 和 `rag_chunks`。

原因是检索发生在 `rag_chunks` 表上。如果权限字段只在 `rag_documents`，每次检索都要 join 文档表。当前为了简单和性能，chunk 表冗余一份权限字段。
