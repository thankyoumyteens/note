# 修改 RagQueryService，接入上下文预算

让 RAG 查询不再无脑拼接所有 chunks，而是经过预算选择。

RAG 里的 context 应该被治理：

```text
高分 chunk 优先
低分 chunk 可丢弃
超长 chunk 可压缩
最终 context 不超过预算
```

### 代码

在 `RagQueryService` 注入：

```java
private final TokenEstimator tokenEstimator;
private final ContextBudgetService contextBudgetService;
private final ContextCompressor contextCompressor;
```

构造器增加：

```java
public RagQueryService(
        EmbeddingClient embeddingClient,
        RagChunkRepository chunkRepository,
        LlmClient llmClient,
        QueryRewriteService queryRewriteService,
        RagProperties ragProperties,
        TokenEstimator tokenEstimator,
        ContextBudgetService contextBudgetService,
        ContextCompressor contextCompressor
) {
    this.embeddingClient = embeddingClient;
    this.chunkRepository = chunkRepository;
    this.llmClient = llmClient;
    this.queryRewriteService = queryRewriteService;
    this.ragProperties = ragProperties;
    this.tokenEstimator = tokenEstimator;
    this.contextBudgetService = contextBudgetService;
    this.contextCompressor = contextCompressor;
}
```

新增方法：

```java
private ContextPackResult packRagContext(List<RagRetrievedChunk> chunks) {
    List<ContextItem> candidates = new ArrayList<>();

    for (RagRetrievedChunk chunk : chunks) {
        String compressedContent = contextCompressor.compressIfNeeded(
                chunk.content(),
                800
        );

        int tokenCount = tokenEstimator.estimate(compressedContent);

        int priority = (int) Math.round(chunk.score() * 100);

        candidates.add(
                new ContextItem(
                        ContextItemType.RAG_CHUNK,
                        compressedContent,
                        priority,
                        tokenCount,
                        Map.of(
                                "documentId", chunk.documentId().toString(),
                                "chunkIndex", chunk.chunkIndex(),
                                "citationId", chunk.citationId(),
                                "score", chunk.score()
                        )
                )
        );
    }

    return contextBudgetService.pack(
            candidates,
            contextBudgetService.ragBudget()
    );
}
```

然后在调用 LLM 前：

```java
ContextPackResult contextPackResult = packRagContext(chunks);

String answer = llmClient.complete(
        buildSystemPrompt(),
        buildUserPrompt(originalQuestion, contextPackResult),
        LlmCallType.COMPLETE
);
```

修改 `buildUserPrompt`：

```java
private String buildUserPrompt(
        String question,
        ContextPackResult contextPackResult
) {
    StringBuilder context = new StringBuilder();

    for (ContextItem item : contextPackResult.selectedItems()) {
        context.append("[")
                .append(item.metadata().get("citationId"))
                .append("]\n")
                .append("documentId=")
                .append(item.metadata().get("documentId"))
                .append(", chunkIndex=")
                .append(item.metadata().get("chunkIndex"))
                .append(", score=")
                .append(item.metadata().get("score"))
                .append("\n")
                .append(item.content())
                .append("\n\n");
    }

    return """
            Question:
            %s

            Context:
            %s

            Context packing info:
            totalTokens=%d
            truncated=%s
            droppedItems=%d
            """.formatted(
            question,
            context,
            contextPackResult.totalTokens(),
            contextPackResult.truncated(),
            contextPackResult.droppedItems().size()
    );
}
```

需要 import：

```java
import com.example.aigateway.context.dto.ContextItem;
import com.example.aigateway.context.dto.ContextItemType;
import com.example.aigateway.context.dto.ContextPackResult;
import com.example.aigateway.context.service.ContextBudgetService;
import com.example.aigateway.context.service.ContextCompressor;
import com.example.aigateway.context.service.TokenEstimator;
import java.util.Map;
```

### 代码说明

现在 RAG context 会经过：

```text
compressIfNeeded
estimate token
priority 排序
budget pack
```

课程阶段可以把 packing info 放 prompt 里帮助调试；生产阶段可以只记日志。
