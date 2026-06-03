# 修改 RagDocumentRepository

保存文档时写入权限字段。

文档权限不应该只在上传接口临时存在，必须持久化到数据库。

#### 代码

修改：

```text
src/main/java/com/example/aigateway/rag/repository/RagDocumentRepository.java
```

```java
package com.example.aigateway.rag.repository;

import com.example.aigateway.rag.dto.RagDocumentVisibility;
import java.sql.Array;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;
import java.util.UUID;
import javax.sql.DataSource;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

@Repository
public class RagDocumentRepository {

    private final JdbcTemplate jdbcTemplate;
    private final DataSource dataSource;

    public RagDocumentRepository(
            JdbcTemplate jdbcTemplate,
            DataSource dataSource
    ) {
        this.jdbcTemplate = jdbcTemplate;
        this.dataSource = dataSource;
    }

    public void save(
            UUID id,
            String filename,
            String contentType,
            String tenantId,
            String ownerUserId,
            RagDocumentVisibility visibility,
            List<String> allowedRoles,
            List<String> allowedUsers
    ) {
        jdbcTemplate.update(connection -> {
            var ps = connection.prepareStatement(
                    """
                    INSERT INTO rag_documents (
                        id,
                        filename,
                        content_type,
                        tenant_id,
                        owner_user_id,
                        visibility,
                        allowed_roles,
                        allowed_users
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """
            );

            ps.setObject(1, id);
            ps.setString(2, filename);
            ps.setString(3, contentType);
            ps.setString(4, tenantId);
            ps.setString(5, ownerUserId);
            ps.setString(6, visibility.name());
            ps.setArray(7, toTextArray(connection, allowedRoles));
            ps.setArray(8, toTextArray(connection, allowedUsers));

            return ps;
        });
    }

    private Array toTextArray(Connection connection, List<String> values) throws SQLException {
        List<String> safeValues = values == null ? List.of() : values;
        return connection.createArrayOf("text", safeValues.toArray(new String[0]));
    }
}
```
