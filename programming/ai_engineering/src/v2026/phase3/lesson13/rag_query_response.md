# 修改 RagQueryResponse

让响应里能看到 RAG 内部判断结果，方便调试。

RAG 不是黑盒。你需要能看到：

```text
原始问题有没有被改写
检索到哪些 chunk
系统是否认为 context 足够
```

#### 代码

修改：

```text
src/main/java/com/example/aigateway/rag/dto/RagQueryResponse.java
```

```java
package com.example.aigateway.rag.dto;

import java.util.List;

/**
 * RAG 查询响应。
 *
 * answer：最终回答
 * chunks：检索到的上下文片段
 * rewrittenQuestion：改写后的查询
 * hasEnoughContext：系统是否认为检索结果足以回答
 */
public record RagQueryResponse(
        String answer,
        List<RagRetrievedChunk> chunks,
        String rewrittenQuestion,
        boolean hasEnoughContext
) {
}
```

#### 代码说明

这会改变第 11 课接口响应结构。属于兼容性变化，但当前还在课程项目阶段，可以接受。
