# 新增 OpenAI-compatible Embedding 实现

调用 OpenAI-compatible `/v1/embeddings` 接口，把文本转成向量。

Embedding API 的输入输出大致是：

```text
input text
  -> embedding model
  -> vector: [0.01, -0.02, ...]
```

这个向量后续会写入 pgvector。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/rag/embedding/OpenAiCompatibleEmbeddingClient.java
```

```java
package com.example.aigateway.rag.embedding;

import java.util.List;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

/**
 * OpenAI-compatible embedding client。
 */
@Component
public class OpenAiCompatibleEmbeddingClient implements EmbeddingClient {

    private final WebClient webClient;
    private final EmbeddingProperties properties;

    public OpenAiCompatibleEmbeddingClient(EmbeddingProperties properties) {
        this.properties = properties;
        this.webClient = WebClient.builder()
                .baseUrl(properties.getBaseUrl())
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + properties.getApiKey())
                .build();
    }

    @Override
    public List<Double> embed(String text) {
        if (text == null || text.isBlank()) {
            throw new IllegalArgumentException("text cannot be empty");
        }

        EmbeddingRequest request = new EmbeddingRequest(
                properties.getModel(),
                text
        );

        EmbeddingResponse response = webClient.post()
                .uri("/v1/embeddings")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(EmbeddingResponse.class)
                .block();

        if (response == null || response.data() == null || response.data().isEmpty()) {
            throw new IllegalStateException("Embedding response is empty");
        }

        List<Double> embedding = response.data().get(0).embedding();

        if (embedding == null || embedding.isEmpty()) {
            throw new IllegalStateException("Embedding vector is empty");
        }

        if (embedding.size() != properties.getDimension()) {
            throw new IllegalStateException(
                    "Embedding dimension mismatch. expected="
                            + properties.getDimension()
                            + ", actual="
                            + embedding.size()
            );
        }

        return embedding;
    }

    public record EmbeddingRequest(
            String model,
            String input
    ) {
    }

    public record EmbeddingResponse(
            List<EmbeddingData> data
    ) {
    }

    public record EmbeddingData(
            int index,
            List<Double> embedding
    ) {
    }
}
```
