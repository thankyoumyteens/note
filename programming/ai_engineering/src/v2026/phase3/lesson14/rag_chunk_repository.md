# 修改 RagChunkRepository

保存 chunk 时也写入权限字段，便于检索时直接过滤。

RAG 检索直接查 `rag_chunks`，所以 chunk 表必须有权限字段。

#### 代码

修改 `save(...)` 方法：

```java
public void save(
        UUID id,
        UUID documentId,
        int chunkIndex,
        String content,
        List<Double> embedding,
        String tenantId,
        String ownerUserId,
        RagDocumentVisibility visibility,
        List<String> allowedRoles,
        List<String> allowedUsers
) {
    jdbcTemplate.update(connection -> {
        var ps = connection.prepareStatement(
                """
                INSERT INTO rag_chunks (
                    id,
                    document_id,
                    chunk_index,
                    content,
                    embedding,
                    tenant_id,
                    owner_user_id,
                    visibility,
                    allowed_roles,
                    allowed_users
                )
                VALUES (?, ?, ?, ?, ?::vector, ?, ?, ?, ?, ?)
                """
        );

        ps.setObject(1, id);
        ps.setObject(2, documentId);
        ps.setInt(3, chunkIndex);
        ps.setString(4, content);
        ps.setString(5, toPgVector(embedding));
        ps.setString(6, tenantId);
        ps.setString(7, ownerUserId);
        ps.setString(8, visibility.name());
        ps.setArray(9, toTextArray(connection, allowedRoles));
        ps.setArray(10, toTextArray(connection, allowedUsers));

        return ps;
    });
}
```

确认 repository 中有：

```java
private Array toTextArray(Connection connection, List<String> values) throws SQLException {
    List<String> safeValues = values == null ? List.of() : values;
    return connection.createArrayOf("text", safeValues.toArray(new String[0]));
}
```

需要 import：

```java
import com.example.aigateway.rag.dto.RagDocumentVisibility;
import java.sql.Array;
import java.sql.Connection;
import java.sql.SQLException;
```
