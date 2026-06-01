# 新增 Spring AI RAG DTO

给 Spring AI Demo 单独定义 DTO，不复用第 11 课 DTO，避免两个实现耦合。

Demo 代码也要有边界。第 12 课是适配层，不要污染第 11 课主线包。

#### 代码

目录：

```text
src/main/java/com/example/aigateway/springai/rag/dto/
```

`SpringAiRagUploadResponse.java`

```java
package com.example.aigateway.springai.rag.dto;

/**
 * Spring AI RAG 文档上传响应。
 */
public record SpringAiRagUploadResponse(
        int documentCount
) {
}
```

`SpringAiRagQueryRequest.java`

```java
package com.example.aigateway.springai.rag.dto;

/**
 * Spring AI RAG 查询请求。
 */
public record SpringAiRagQueryRequest(
        String question,
        Integer topK
) {
}
```

`SpringAiRetrievedDocument.java`

```java
package com.example.aigateway.springai.rag.dto;

import java.util.Map;

/**
 * Spring AI 检索结果 DTO。
 */
public record SpringAiRetrievedDocument(
        String text,
        Map<String, Object> metadata
) {
}
```

`SpringAiRagQueryResponse.java`

```java
package com.example.aigateway.springai.rag.dto;

import java.util.List;

/**
 * Spring AI RAG 查询响应。
 */
public record SpringAiRagQueryResponse(
        String answer,
        List<SpringAiRetrievedDocument> documents
) {
}
```

#### 代码说明

这里返回 `documents` 而不是 `chunks`，是为了贴近 Spring AI 的 `Document` 抽象。
