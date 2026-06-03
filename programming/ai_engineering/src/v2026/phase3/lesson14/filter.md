# 修改 RagChunkRepository 检索逻辑，加入权限过滤

让 RAG 查询只能检索当前用户有权限访问的 chunk。

权限过滤条件：

```text
tenant_id = 当前租户
并且满足以下任一条件：
1. visibility = TENANT
2. visibility = PRIVATE 且 owner_user_id = 当前用户
3. visibility = ROLE 且 allowed_roles 和当前用户 roles 有交集
4. visibility = USER 且 allowed_users 包含当前用户
```

PostgreSQL 数组交集可以用：

```sql
allowed_roles && ?::text[]
```

数组包含可以用：

```sql
? = ANY(allowed_users)
```

#### 代码

在 `RagChunkRepository` 中新增方法，替代第 13 课的 `hybridSearch`：

```java
public List<RagRetrievedChunk> hybridSearchWithPermission(
        List<Double> queryEmbedding,
        String queryText,
        int topK,
        double vectorWeight,
        double keywordWeight,
        String tenantId,
        String userId,
        List<String> roles
) {
    String vector = toPgVector(queryEmbedding);
    String keyword = queryText == null ? "" : queryText.strip();

    return jdbcTemplate.query(connection -> {
        var ps = connection.prepareStatement(
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
                WHERE tenant_id = ?
                  AND (
                    visibility = 'TENANT'
                    OR (visibility = 'PRIVATE' AND owner_user_id = ?)
                    OR (visibility = 'ROLE' AND allowed_roles && ?::text[])
                    OR (visibility = 'USER' AND ? = ANY(allowed_users))
                  )
                ORDER BY score DESC
                LIMIT ?
                """
        );

        ps.setString(1, vector);
        ps.setDouble(2, vectorWeight);
        ps.setString(3, keyword);
        ps.setDouble(4, keywordWeight);
        ps.setString(5, tenantId);
        ps.setString(6, userId);
        ps.setArray(7, toTextArray(connection, roles));
        ps.setString(8, userId);
        ps.setInt(9, topK);

        return ps;
    }, (rs, rowNum) -> new RagRetrievedChunk(
            rs.getObject("document_id", UUID.class),
            rs.getInt("chunk_index"),
            rs.getString("content"),
            rs.getDouble("score"),
            null
    ));
}
```

#### 代码说明

最关键的是 `WHERE`：

```sql
WHERE tenant_id = ?
  AND (
    visibility = 'TENANT'
    OR (visibility = 'PRIVATE' AND owner_user_id = ?)
    OR (visibility = 'ROLE' AND allowed_roles && ?::text[])
    OR (visibility = 'USER' AND ? = ANY(allowed_users))
  )
```

这保证不同租户之间不会互相检索。
