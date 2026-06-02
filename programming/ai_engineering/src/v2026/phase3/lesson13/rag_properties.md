# 新增 RagProperties

把 RAG 的质量参数从代码里抽出来，避免写死。

RAG 质量不是固定的。不同项目需要调这些参数：

```text
topK 默认值
最低相似度阈值
向量分数权重
关键词分数权重
是否启用 query rewrite
是否启用 no-answer
```

这些都应该放到配置里。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/rag/config/RagProperties.java
```

```java
package com.example.aigateway.rag.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * RAG 质量增强相关配置。
 *
 * 第 13 课开始，RAG 不再只追求“能回答”，
 * 而是要逐步追求：
 * - 检索更准
 * - 不知道时拒答
 * - 回答能追溯来源
 * - 参数可调
 */
@ConfigurationProperties(prefix = "ai.rag")
public class RagProperties {

    /**
     * 默认检索条数。
     */
    private int defaultTopK = 5;

    /**
     * 最大检索条数，防止一次塞太多 context。
     */
    private int maxTopK = 10;

    /**
     * 最低 context 分数。
     *
     * 如果 top chunk 的分数低于该阈值，
     * 说明检索结果很可能不相关，应触发 no-answer。
     */
    private double minContextScore = 0.3;

    /**
     * 向量相似度权重。
     */
    private double vectorWeight = 0.7;

    /**
     * 关键词命中权重。
     */
    private double keywordWeight = 0.3;

    /**
     * 是否启用 query rewrite。
     */
    private boolean queryRewriteEnabled = true;

    /**
     * 是否启用 no-answer 判断。
     */
    private boolean noAnswerEnabled = true;

    public int getDefaultTopK() {
        return defaultTopK;
    }

    public void setDefaultTopK(int defaultTopK) {
        this.defaultTopK = defaultTopK;
    }

    public int getMaxTopK() {
        return maxTopK;
    }

    public void setMaxTopK(int maxTopK) {
        this.maxTopK = maxTopK;
    }

    public double getMinContextScore() {
        return minContextScore;
    }

    public void setMinContextScore(double minContextScore) {
        this.minContextScore = minContextScore;
    }

    public double getVectorWeight() {
        return vectorWeight;
    }

    public void setVectorWeight(double vectorWeight) {
        this.vectorWeight = vectorWeight;
    }

    public double getKeywordWeight() {
        return keywordWeight;
    }

    public void setKeywordWeight(double keywordWeight) {
        this.keywordWeight = keywordWeight;
    }

    public boolean isQueryRewriteEnabled() {
        return queryRewriteEnabled;
    }

    public void setQueryRewriteEnabled(boolean queryRewriteEnabled) {
        this.queryRewriteEnabled = queryRewriteEnabled;
    }

    public boolean isNoAnswerEnabled() {
        return noAnswerEnabled;
    }

    public void setNoAnswerEnabled(boolean noAnswerEnabled) {
        this.noAnswerEnabled = noAnswerEnabled;
    }
}
```

启动类增加：

```java
@EnableConfigurationProperties({
        LlmProperties.class,
        RateLimitProperties.class,
        EmbeddingProperties.class,
        RagProperties.class
})
```

`application.yml` 增加：

```yaml
ai:
  rag:
    default-top-k: 5
    max-top-k: 10
    min-context-score: 0.3
    vector-weight: 0.7
    keyword-weight: 0.3
    query-rewrite-enabled: true
    no-answer-enabled: true
```

#### 代码说明

本课先用简单权重：

```text
finalScore = vectorScore * 0.7 + keywordScore * 0.3
```

后续可以通过 eval 调整这些参数。
