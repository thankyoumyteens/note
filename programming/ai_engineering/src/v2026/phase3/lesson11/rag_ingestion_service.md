# 新增 RagIngestionService

实现上传文档后的入库流程。

Ingestion 是 RAG 的“离线”或“准实时”流程：

```text
文档 -> 文本 -> chunk -> embedding -> vector DB
```

用户提问时不会重新处理整篇文档，只会检索已入库 chunk。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/rag/service/RagIngestionService.java
```

```java
package com.example.aigateway.rag.service;

import com.example.aigateway.rag.dto.RagUploadResponse;
import com.example.aigateway.rag.embedding.EmbeddingClient;
import com.example.aigateway.rag.repository.RagChunkRepository;
import com.example.aigateway.rag.repository.RagDocumentRepository;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.UUID;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class RagIngestionService {

    private final TextChunker textChunker;
    private final EmbeddingClient embeddingClient;
    private final RagDocumentRepository documentRepository;
    private final RagChunkRepository chunkRepository;

    public RagIngestionService(
            TextChunker textChunker,
            EmbeddingClient embeddingClient,
            RagDocumentRepository documentRepository,
            RagChunkRepository chunkRepository
    ) {
        this.textChunker = textChunker;
        this.embeddingClient = embeddingClient;
        this.documentRepository = documentRepository;
        this.chunkRepository = chunkRepository;
    }

    public RagUploadResponse upload(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new IllegalArgumentException("file cannot be empty");
        }

        try {
            String text = new String(file.getBytes(), StandardCharsets.UTF_8);

            List<String> chunks = textChunker.chunk(text);

            UUID documentId = UUID.randomUUID();

            documentRepository.save(
                    documentId,
                    file.getOriginalFilename() == null ? "unknown.txt" : file.getOriginalFilename(),
                    file.getContentType()
            );

            for (int i = 0; i < chunks.size(); i++) {
                String chunk = chunks.get(i);
                List<Double> embedding = embeddingClient.embed(chunk);

                chunkRepository.save(
                        UUID.randomUUID(),
                        documentId,
                        i,
                        chunk,
                        embedding
                );
            }

            return new RagUploadResponse(
                    documentId,
                    file.getOriginalFilename(),
                    chunks.size()
            );

        } catch (Exception e) {
            throw new RuntimeException("Failed to ingest document", e);
        }
    }
}
```

本课只支持 `.txt` 或纯文本内容。PDF、Word 解析放后续 Python 文档处理或 RAG 增强课程。
