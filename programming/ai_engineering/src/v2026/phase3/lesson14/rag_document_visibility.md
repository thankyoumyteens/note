# 新增 RagDocumentVisibility

用枚举表达文档可见性，避免到处写字符串。

权限字段不要散落成：

```text
"private"
"PRIVATE"
"role"
"ROLE"
```

统一用 enum，减少拼写错误。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/rag/dto/RagDocumentVisibility.java
```

```java
package com.example.aigateway.rag.dto;

/**
 * RAG 文档可见性。
 *
 * PRIVATE：仅上传者可见
 * TENANT：同租户所有用户可见
 * ROLE：指定角色可见
 * USER：指定用户可见
 */
public enum RagDocumentVisibility {
    PRIVATE,
    TENANT,
    ROLE,
    USER
}
```
