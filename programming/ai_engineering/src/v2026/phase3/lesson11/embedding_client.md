# 新增 EmbeddingClient

给 embedding 调用建立抽象，避免业务代码直接依赖具体供应商。

和 `LlmClient` 一样，embedding 也需要抽象：

```text
业务代码 -> EmbeddingClient -> 具体 embedding provider
```

#### 代码

文件：

```text
src/main/java/com/example/aigateway/rag/embedding/EmbeddingClient.java
```

```java
package com.example.aigateway.rag.embedding;

import java.util.List;

/**
 * Embedding 调用抽象。
 *
 * 输入文本，返回向量。
 */
public interface EmbeddingClient {

    /**
     * 将单段文本转换成向量。
     */
    List<Double> embed(String text);
}
```
