# 新增 SpringAiRagService

用 Spring AI 的 `VectorStore` 实现一个独立 RAG Demo。

Spring AI 的 `VectorStore` 负责：

```text
add documents
similarity search
```

`Document` 是 Spring AI 中表示文本和元数据的对象。`VectorStore` 负责把 `Document` 存入向量库并检索回来。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/springai/rag/service/SpringAiRagService.java
```

代码：

```java
package com.example.aigateway.springai.rag.service;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.dto.LlmCallType;
import com.example.aigateway.springai.rag.dto.SpringAiRagQueryRequest;
import com.example.aigateway.springai.rag.dto.SpringAiRagQueryResponse;
import com.example.aigateway.springai.rag.dto.SpringAiRagUploadResponse;
import com.example.aigateway.springai.rag.dto.SpringAiRetrievedDocument;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

/**
 * Spring AI RAG Demo 服务。
 *
 * 重要：
 * - 这是第 12 课的框架适配 Demo。
 * - 不替换第 11 课手写 RAG 主线。
 * - 业务主线仍然保留自己的 RagIngestionService / RagQueryService。
 */
@Service
public class SpringAiRagService {

    private final VectorStore vectorStore;
    private final LlmClient llmClient;

    public SpringAiRagService(
            VectorStore vectorStore,
            LlmClient llmClient
    ) {
        this.vectorStore = vectorStore;
        this.llmClient = llmClient;
    }

    /**
     * 上传纯文本文件，并使用 Spring AI VectorStore 入库。
     */
    public SpringAiRagUploadResponse upload(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new IllegalArgumentException("file cannot be empty");
        }

        try {
            String text = new String(file.getBytes(), StandardCharsets.UTF_8);

            // 第 12 课 Demo：这里先把整个文本作为一个 Document。
            // 更细的 chunking 已在第 11 课手写实现中完成。
            // 后续第 13 课再系统优化 chunking / rerank / hybrid search。
            Document document = new Document(
                    text,
                    Map.of(
                            "filename", file.getOriginalFilename() == null ? "unknown.txt" : file.getOriginalFilename(),
                            "source", "spring-ai-rag-demo"
                    )
            );

            vectorStore.add(List.of(document));

            return new SpringAiRagUploadResponse(1);

        } catch (Exception e) {
            throw new RuntimeException("Failed to upload document to Spring AI VectorStore", e);
        }
    }

    /**
     * 使用 Spring AI VectorStore 检索，再调用统一 LlmClient 回答。
     */
    public SpringAiRagQueryResponse query(SpringAiRagQueryRequest request) {
        if (request == null || request.question() == null || request.question().isBlank()) {
            throw new IllegalArgumentException("question cannot be empty");
        }

        int topK = request.topK() == null ? 5 : request.topK();

        if (topK <= 0 || topK > 10) {
            throw new IllegalArgumentException("topK must be between 1 and 10");
        }

        SearchRequest searchRequest = SearchRequest.builder()
                .query(request.question())
                .topK(topK)
                .build();

        List<Document> documents = vectorStore.similaritySearch(searchRequest);

        if (documents == null) {
            documents = List.of();
        }

        String answer = llmClient.complete(
                buildSystemPrompt(),
                buildUserPrompt(request.question(), documents),
                LlmCallType.COMPLETE
        );

        List<SpringAiRetrievedDocument> retrievedDocuments = new ArrayList<>();

        for (Document document : documents) {
            retrievedDocuments.add(
                    new SpringAiRetrievedDocument(
                            document.getText(),
                            document.getMetadata()
                    )
            );
        }

        return new SpringAiRagQueryResponse(
                answer,
                retrievedDocuments
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

    private String buildUserPrompt(String question, List<Document> documents) {
        StringBuilder context = new StringBuilder();

        for (int i = 0; i < documents.size(); i++) {
            Document document = documents.get(i);

            context.append("[Document ")
                    .append(i + 1)
                    .append("]\n")
                    .append(document.getText())
                    .append("\n")
                    .append("metadata=")
                    .append(document.getMetadata())
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

这里刻意仍然使用你的 `LlmClient`，而不是直接让业务服务依赖 Spring AI `ChatClient`。

原因是第 9 课已经确定架构边界：

```text
Controller
  -> Service
  -> LlmClient
  -> OpenAiCompatibleLlmClient / SpringAiLlmClient
```

Spring AI 在本课只负责 `VectorStore` 适配，不侵入主线业务服务。
