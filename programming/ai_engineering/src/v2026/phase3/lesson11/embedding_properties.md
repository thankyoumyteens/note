# 新增 EmbeddingProperties

把 embedding 配置绑定成 Java 对象。

你之前已经做过 `LlmProperties`。这里是同样思路，只是目标从 chat model 变成 embedding model。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/rag/embedding/EmbeddingProperties.java
```

```java
package com.example.aigateway.rag.embedding;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * Embedding 模型配置。
 */
@ConfigurationProperties(prefix = "ai.embedding")
public class EmbeddingProperties {

    private String baseUrl;
    private String apiKey;
    private String model;
    private int dimension = 1536;

    public String getBaseUrl() {
        return baseUrl;
    }

    public void setBaseUrl(String baseUrl) {
        this.baseUrl = baseUrl;
    }

    public String getApiKey() {
        return apiKey;
    }

    public void setApiKey(String apiKey) {
        this.apiKey = apiKey;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public int getDimension() {
        return dimension;
    }

    public void setDimension(int dimension) {
        this.dimension = dimension;
    }
}
```

然后在启动类启用：

```java
@EnableConfigurationProperties({
        LlmProperties.class,
        RateLimitProperties.class,
        EmbeddingProperties.class
})
```
