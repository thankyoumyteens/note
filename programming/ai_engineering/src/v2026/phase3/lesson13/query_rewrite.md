# 新增 query rewrite 服务

把用户口语化问题改写成更适合检索的问题。

用户问题可能很口语：

```text
这个东西到底是怎么减少胡编的？
```

但文档里写的是：

```text
RAG 可以降低模型幻觉。
```

Query rewrite 的目标是把问题改写成更适合检索的形式：

```text
RAG 如何降低大语言模型幻觉？
```

#### 代码

文件：

```text
src/main/java/com/example/aigateway/rag/service/QueryRewriteService.java
```

```java
package com.example.aigateway.rag.service;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.dto.LlmCallType;
import com.example.aigateway.rag.config.RagProperties;
import org.springframework.stereotype.Service;

/**
 * 查询改写服务。
 *
 * 作用：
 * - 把用户口语化问题改写成更适合向量检索的问题
 * - 保留原意，不扩写答案
 * - 不引入文档中不存在的信息
 */
@Service
public class QueryRewriteService {

    private final LlmClient llmClient;
    private final RagProperties ragProperties;

    public QueryRewriteService(
            LlmClient llmClient,
            RagProperties ragProperties
    ) {
        this.llmClient = llmClient;
        this.ragProperties = ragProperties;
    }

    public String rewrite(String question) {
        if (question == null || question.isBlank()) {
            throw new IllegalArgumentException("question cannot be empty");
        }

        if (!ragProperties.isQueryRewriteEnabled()) {
            return question.strip();
        }

        String systemPrompt = """
                你是一个 RAG 查询改写器。

                任务：
                - 把用户问题改写成更适合知识库检索的查询。
                - 保留原始问题含义。
                - 不要回答问题。
                - 不要添加用户没有问的新意图。
                - 只输出改写后的查询文本。
                """;

        String userPrompt = """
                原始问题：
                %s
                """.formatted(question);

        String rewritten = llmClient.complete(
                systemPrompt,
                userPrompt,
                LlmCallType.COMPLETE
        );

        if (rewritten == null || rewritten.isBlank()) {
            return question.strip();
        }

        return rewritten.strip();
    }
}
```

#### 代码说明

这里继续使用 `LlmClient`，不绕过你之前的 AI Gateway 抽象。
