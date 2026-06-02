# 修改 RagQueryService

RAG v2 查询流程：

```text
question
  -> rewrite
  -> embedding(rewrittenQuestion)
  -> hybridSearch
  -> check context score
  -> add citationId
  -> build prompt
  -> LLM answer
```

#### 代码

修改：

```text
src/main/java/com/example/aigateway/rag/service/RagQueryService.java
```

参考实现：

```java
package com.example.aigateway.rag.service;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.dto.LlmCallType;
import com.example.aigateway.rag.config.RagProperties;
import com.example.aigateway.rag.dto.RagQueryRequest;
import com.example.aigateway.rag.dto.RagQueryResponse;
import com.example.aigateway.rag.dto.RagRetrievedChunk;
import com.example.aigateway.rag.embedding.EmbeddingClient;
import com.example.aigateway.rag.repository.RagChunkRepository;
import java.util.ArrayList;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class RagQueryService {

    private final EmbeddingClient embeddingClient;
    private final RagChunkRepository chunkRepository;
    private final LlmClient llmClient;
    private final QueryRewriteService queryRewriteService;
    private final RagProperties ragProperties;

    public RagQueryService(
            EmbeddingClient embeddingClient,
            RagChunkRepository chunkRepository,
            LlmClient llmClient,
            QueryRewriteService queryRewriteService,
            RagProperties ragProperties
    ) {
        this.embeddingClient = embeddingClient;
        this.chunkRepository = chunkRepository;
        this.llmClient = llmClient;
        this.queryRewriteService = queryRewriteService;
        this.ragProperties = ragProperties;
    }

    public RagQueryResponse query(RagQueryRequest request) {
        if (request == null || request.question() == null || request.question().isBlank()) {
            throw new IllegalArgumentException("question cannot be empty");
        }

        int topK = resolveTopK(request.topK());

        String originalQuestion = request.question().strip();

        /*
         * Step 1：Query Rewrite
         *
         * 把用户原始问题改写成更适合检索的问题。
         * 如果关闭 rewrite 或改写失败，则回退原问题。
         */
        String rewrittenQuestion = queryRewriteService.rewrite(originalQuestion);

        /*
         * Step 2：Embedding
         *
         * 注意：这里对 rewrittenQuestion 做 embedding，
         * 因为它通常比原始口语化问题更适合检索。
         */
        List<Double> questionEmbedding = embeddingClient.embed(rewrittenQuestion);

        /*
         * Step 3：Hybrid Search
         *
         * 使用向量相似度 + 简单关键词命中融合。
         */
        List<RagRetrievedChunk> rawChunks = chunkRepository.hybridSearch(
                questionEmbedding,
                rewrittenQuestion,
                topK,
                ragProperties.getVectorWeight(),
                ragProperties.getKeywordWeight()
        );

        /*
         * Step 4：Citation
         *
         * 给检索结果按当前排序补引用编号。
         */
        List<RagRetrievedChunk> chunks = addCitationIds(rawChunks);

        /*
         * Step 5：No-answer 判断
         *
         * 如果检索结果为空，或者最高分低于阈值，则不让模型硬答。
         */
        boolean hasEnoughContext = hasEnoughContext(chunks);

        if (!hasEnoughContext) {
            return new RagQueryResponse(
                    "根据已提供文档无法确定。",
                    chunks,
                    rewrittenQuestion,
                    false
            );
        }

        /*
         * Step 6：LLM 基于 context 回答
         */
        String answer = llmClient.complete(
                buildSystemPrompt(),
                buildUserPrompt(originalQuestion, chunks),
                LlmCallType.COMPLETE
        );

        return new RagQueryResponse(
                answer,
                chunks,
                rewrittenQuestion,
                true
        );
    }

    private int resolveTopK(Integer topK) {
        int value = topK == null ? ragProperties.getDefaultTopK() : topK;

        if (value <= 0 || value > ragProperties.getMaxTopK()) {
            throw new IllegalArgumentException(
                    "topK must be between 1 and " + ragProperties.getMaxTopK()
            );
        }

        return value;
    }

    private List<RagRetrievedChunk> addCitationIds(List<RagRetrievedChunk> chunks) {
        List<RagRetrievedChunk> result = new ArrayList<>();

        for (int i = 0; i < chunks.size(); i++) {
            result.add(chunks.get(i).withCitationId(i + 1));
        }

        return result;
    }

    private boolean hasEnoughContext(List<RagRetrievedChunk> chunks) {
        if (!ragProperties.isNoAnswerEnabled()) {
            return true;
        }

        if (chunks == null || chunks.isEmpty()) {
            return false;
        }

        double topScore = chunks.get(0).score();

        return topScore >= ragProperties.getMinContextScore();
    }

    private String buildSystemPrompt() {
        return """
                你是一个企业知识库问答助手。

                你必须只基于用户提供的 Context 回答问题。

                规则：
                - 如果 Context 中没有答案，请回答：根据已提供文档无法确定。
                - 不要编造文档中不存在的信息。
                - 回答要简洁、准确。
                - 如果引用了某段 Context，请在句末使用对应编号，例如 [1]、[2]。
                """;
    }

    private String buildUserPrompt(
            String question,
            List<RagRetrievedChunk> chunks
    ) {
        StringBuilder context = new StringBuilder();

        for (RagRetrievedChunk chunk : chunks) {
            context.append("[")
                    .append(chunk.citationId())
                    .append("]\n")
                    .append("documentId=")
                    .append(chunk.documentId())
                    .append(", chunkIndex=")
                    .append(chunk.chunkIndex())
                    .append(", score=")
                    .append(chunk.score())
                    .append("\n")
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

#### 代码说明

这一版做了 4 个增强：

```text
query rewrite：改写问题
hybrid search：混合检索
no-answer：低置信度拒答
citation：给 context 编号
```
