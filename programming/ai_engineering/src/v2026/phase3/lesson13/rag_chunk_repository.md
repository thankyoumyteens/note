# 修改 RagChunkRepository，支持 Hybrid Search

让检索不再只靠向量相似度，而是融合关键词命中。

Vector Search 擅长语义相似：

```text
“胡编” ≈ “幻觉”
```

Keyword Search 擅长精确词命中：

```text
Spring AI
pgvector
BAAI/bge-large-zh-v1.5
```

Hybrid Search 的目的就是把两者结合起来。

#### 代码

修改：

```text
src/main/java/com/example/aigateway/rag/repository/RagChunkRepository.java
```

增加方法：

```java
public List<RagRetrievedChunk> hybridSearch(
        List<Double> queryEmbedding,
        String queryText,
        int topK,
        double vectorWeight,
        double keywordWeight
) {
    String vector = toPgVector(queryEmbedding);
    String keyword = queryText == null ? "" : queryText.strip();

    /*
     * 说明：
     * - vector_score = 1 - cosine_distance
     * - keyword_score 先用简单 ILIKE 命中做入门版
     * - final score = vector_score * vectorWeight + keyword_score * keywordWeight
     *
     * 注意：
     * PostgreSQL 原生中文全文检索比较复杂。
     * 第 13 课先用简单 keyword_score 理解 hybrid search 思路。
     * 后续如果要做生产级中文检索，应考虑 Elasticsearch / OpenSearch / 专门中文分词方案。
     */
    return jdbcTemplate.query(
            """
            SELECT
                document_id,
                chunk_index,
                content,
                (
                    (1 - (embedding <=> ?::vector)) * ?
                    +
                    (
                        CASE
                            WHEN content ILIKE '%' || ? || '%' THEN 1.0
                            ELSE 0.0
                        END
                    ) * ?
                ) AS score
            FROM rag_chunks
            ORDER BY score DESC
            LIMIT ?
            """,
            (rs, rowNum) -> new RagRetrievedChunk(
                    rs.getObject("document_id", UUID.class),
                    rs.getInt("chunk_index"),
                    rs.getString("content"),
                    rs.getDouble("score"),
                    null
            ),
            vector,
            vectorWeight,
            keyword,
            keywordWeight,
            topK
    );
}
```

如果你原来没有这些 import，确认有：

```java
import com.example.aigateway.rag.dto.RagRetrievedChunk;
import java.util.List;
import java.util.UUID;
```

#### 代码说明

本课的 keyword 部分是入门版：

```sql
-- 判断 content 字段里是否包含 query 这段文本，忽略大小写。
content ILIKE '%' || query || '%'
```

它不完美，但能让你理解 hybrid search 的结构。

更生产的方案放到后续：

```text
Elasticsearch / OpenSearch
中文分词
BM25
向量检索融合
rerank
```
