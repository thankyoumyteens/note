# 修改 RagIngestionService

上传文档时读取当前用户，并把权限字段传给 repository。

文档权限应该在 ingestion 时确定：

```text
谁上传的？
属于哪个租户？
谁可以看？
```

#### 代码

修改 `upload(...)` 方法签名：

```java
public RagUploadResponse upload(
        MultipartFile file,
        RagDocumentVisibility visibility,
        List<String> allowedRoles,
        List<String> allowedUsers
)
```

核心修改参考：

```java
CurrentUserContext currentUser = CurrentUserContextHolder.getRequired();

documentRepository.save(
        documentId,
        file.getOriginalFilename() == null ? "unknown.txt" : file.getOriginalFilename(),
        file.getContentType(),
        currentUser.tenantId(),
        currentUser.userId(),
        visibility,
        allowedRoles,
        allowedUsers
);

for (int i = 0; i < chunks.size(); i++) {
    String chunk = chunks.get(i);
    List<Double> embedding = embeddingClient.embed(chunk);

    chunkRepository.save(
            UUID.randomUUID(),
            documentId,
            i,
            chunk,
            embedding,
            currentUser.tenantId(),
            currentUser.userId(),
            visibility,
            allowedRoles,
            allowedUsers
    );
}
```

需要 import：

```java
import com.example.aigateway.rag.dto.RagDocumentVisibility;
import com.example.aigateway.security.CurrentUserContext;
import com.example.aigateway.security.CurrentUserContextHolder;
```

建议在 service 开头兜底：

```java
if (visibility == null) {
    visibility = RagDocumentVisibility.PRIVATE;
}
```
