# 修改 RagDocumentController

上传接口允许指定文档可见性、允许角色、允许用户。

权限信息属于文档 metadata。上传时需要一起传入。

#### 代码

```java
@PostMapping("/documents")
public RagUploadResponse upload(
        @RequestParam("file") MultipartFile file,
        @RequestParam(value = "visibility", defaultValue = "PRIVATE") RagDocumentVisibility visibility,
        @RequestParam(value = "allowedRoles", required = false) List<String> allowedRoles,
        @RequestParam(value = "allowedUsers", required = false) List<String> allowedUsers
) {
    return ragIngestionService.upload(
            file,
            visibility,
            allowedRoles == null ? List.of() : allowedRoles,
            allowedUsers == null ? List.of() : allowedUsers
    );
}
```

需要 import：

```java
import com.example.aigateway.rag.dto.RagDocumentVisibility;
import java.util.List;
```
