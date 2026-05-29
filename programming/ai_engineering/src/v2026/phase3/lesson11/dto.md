# 新增 DTO

定义上传和查询接口的请求/响应结构。

RAG 接口也必须返回稳定 DTO，不能直接返回杂乱 Map。

#### 代码

目录：

```text
src/main/java/com/example/aigateway/rag/dto/
```

`RagUploadResponse.java`

```java
package com.example.aigateway.rag.dto;

import java.util.UUID;

public record RagUploadResponse(
        UUID documentId,
        String filename,
        int chunkCount
) {
}
```

`RagQueryRequest.java`

```java
package com.example.aigateway.rag.dto;

public record RagQueryRequest(
        String question,
        Integer topK
) {
}
```

`RagRetrievedChunk.java`

```java
package com.example.aigateway.rag.dto;

import java.util.UUID;

public record RagRetrievedChunk(
        UUID documentId,
        int chunkIndex,
        String content,
        double score
) {
}
```

`RagQueryResponse.java`

```java
package com.example.aigateway.rag.dto;

import java.util.List;

public record RagQueryResponse(
        String answer,
        List<RagRetrievedChunk> chunks
) {
}
```
