# 修改 RagRetrievedChunk，增加 citationId

让返回给前端的 chunk 可以被引用。

Citation 的核心不是让模型随便说“参考文档”，而是让系统明确告诉用户：

```text
答案参考了哪些 chunk
chunk 内容是什么
chunk 来自哪个 documentId
chunkIndex 是多少
```

#### 代码

修改：

```text
src/main/java/com/example/aigateway/rag/dto/RagRetrievedChunk.java
```

```java
package com.example.aigateway.rag.dto;

import java.util.UUID;

/**
 * RAG 检索返回的 chunk。
 *
 * citationId 用于回答中的引用编号，例如 [1]、[2]。
 */
public record RagRetrievedChunk(
        UUID documentId,
        int chunkIndex,
        String content,
        double score,
        Integer citationId
) {
    /**
     * 给 chunk 补充 citationId。
     */
    public RagRetrievedChunk withCitationId(int citationId) {
        return new RagRetrievedChunk(
                documentId,
                chunkIndex,
                content,
                score,
                citationId
        );
    }
}
```

#### 代码说明

`citationId` 是展示层编号，不是数据库字段。

例如：

```text
citationId = 1 -> 回答里可以写 [1]
citationId = 2 -> 回答里可以写 [2]
```
