# 新增 Repository

封装文档和 chunk 的数据库读写。

RAG 检索本质是：

```sql
ORDER BY embedding <=> query_embedding
LIMIT topK
```

`<=>` 是 cosine distance。距离越小越相似。

本课返回 `score = 1 - distance`，方便理解为相似度。

#### 代码

`RagDocumentRepository.java`

```java
package com.example.aigateway.rag.repository;

import java.util.UUID;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

@Repository
public class RagDocumentRepository {

    private final JdbcTemplate jdbcTemplate;

    public RagDocumentRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public void save(UUID id, String filename, String contentType) {
        jdbcTemplate.update(
                """
                INSERT INTO rag_documents (id, filename, content_type)
                VALUES (?, ?, ?)
                """,
                id,
                filename,
                contentType
        );
    }
}
```

`RagChunkRepository.java`

```java
package com.example.aigateway.rag.repository;

import com.example.aigateway.rag.dto.RagRetrievedChunk;
import java.util.List;
import java.util.UUID;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

@Repository
public class RagChunkRepository {

    private final JdbcTemplate jdbcTemplate;

    public RagChunkRepository(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    public void save(
            UUID id,
            UUID documentId,
            int chunkIndex,
            String content,
            List<Double> embedding
    ) {
        jdbcTemplate.update(
                """
                INSERT INTO rag_chunks (id, document_id, chunk_index, content, embedding)
                VALUES (?, ?, ?, ?, ?::vector)
                """,
                id,
                documentId,
                chunkIndex,
                content,
                toPgVector(embedding)
        );
    }

    public List<RagRetrievedChunk> searchTopK(
            List<Double> queryEmbedding,
            int topK
    ) {
        String vector = toPgVector(queryEmbedding);

        return jdbcTemplate.query(
                """
                SELECT
                    document_id,
                    chunk_index,
                    content,
                    1 - (embedding <=> ?::vector) AS score
                FROM rag_chunks
                ORDER BY embedding <=> ?::vector
                LIMIT ?
                """,
                (rs, rowNum) -> new RagRetrievedChunk(
                        rs.getObject("document_id", UUID.class),
                        rs.getInt("chunk_index"),
                        rs.getString("content"),
                        rs.getDouble("score")
                ),
                vector,
                vector,
                topK
        );
    }

    private String toPgVector(List<Double> embedding) {
        StringBuilder builder = new StringBuilder();
        builder.append("[");

        for (int i = 0; i < embedding.size(); i++) {
            if (i > 0) {
                builder.append(",");
            }
            builder.append(embedding.get(i));
        }

        builder.append("]");
        return builder.toString();
    }
}
```
