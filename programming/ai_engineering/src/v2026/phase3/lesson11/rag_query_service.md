# 新增 RagQueryService

实现 RAG 查询流程：问题 embedding → top-k 检索 → 组装 context → 调 LLM 回答。

RAG 的核心不是让模型“凭记忆回答”，而是让模型基于检索到的上下文回答。

Prompt 中必须明确：

```text
只基于给定 context 回答
如果 context 不足，就说无法从文档中确定
```

#### 代码

文件：

```text
src/main/java/com/example/aigateway/rag/service/RagQueryService.java
```

```java
package com.example.aigateway.rag.service;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.dto.LlmCallType;
import com.example.aigateway.rag.dto.RagQueryRequest;
import com.example.aigateway.rag.dto.RagQueryResponse;
import com.example.aigateway.rag.dto.RagRetrievedChunk;
import com.example.aigateway.rag.embedding.EmbeddingClient;
import com.example.aigateway.rag.repository.RagChunkRepository;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class RagQueryService {

    private final EmbeddingClient embeddingClient;
    private final RagChunkRepository chunkRepository;
    private final LlmClient llmClient;

    public RagQueryService(
            EmbeddingClient embeddingClient,
            RagChunkRepository chunkRepository,
            LlmClient llmClient
    ) {
        this.embeddingClient = embeddingClient;
        this.chunkRepository = chunkRepository;
        this.llmClient = llmClient;
    }

    public RagQueryResponse query(RagQueryRequest request) {
        if (request == null || request.question() == null || request.question().isBlank()) {
            throw new IllegalArgumentException("question cannot be empty");
        }

        int topK = request.topK() == null ? 5 : request.topK();

        if (topK <= 0 || topK > 10) {
            throw new IllegalArgumentException("topK must be between 1 and 10");
        }

        List<Double> questionEmbedding = embeddingClient.embed(request.question());

        List<RagRetrievedChunk> chunks = chunkRepository.searchTopK(
                questionEmbedding,
                topK
        );

        String answer = llmClient.complete(
                buildSystemPrompt(),
                buildUserPrompt(request.question(), chunks),
                LlmCallType.COMPLETE
        );

        return new RagQueryResponse(
                answer,
                chunks
        );
    }

    private String buildSystemPrompt() {
        return """
                你是一个企业知识库问答助手。

                你必须只基于用户提供的 Context 回答问题。

                规则：
                - 如果 Context 中没有答案，请回答：根据已提供文档无法确定。
                - 不要编造文档中不存在的信息。
                - 回答要简洁、准确。
                """;
    }

    private String buildUserPrompt(
            String question,
            List<RagRetrievedChunk> chunks
    ) {
        StringBuilder context = new StringBuilder();

        for (int i = 0; i < chunks.size(); i++) {
            RagRetrievedChunk chunk = chunks.get(i);

            context.append("[Chunk ")
                    .append(i + 1)
                    .append(", score=")
                    .append(chunk.score())
                    .append("]\n")
                    .append(chunk.content())
                    .append("\n\n");
        }

        return """
                Question:
                %s

                Context:
                %s
                """.formatted(question, context);
    }
}
```
