# 新增 ContextProperties

把上下文预算参数放到配置文件中，避免写死在代码里。

Context Engineering 的核心不是“prompt 写长一点”，而是分配预算：

```text
system prompt 需要多少
用户问题需要多少
RAG context 最多多少
工具结果最多多少
最终回答预留多少
```

### 代码

文件：

```text
src/main/java/com/example/aigateway/context/config/ContextProperties.java
```

```java
package com.example.aigateway.context.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * 上下文工程配置。
 *
 * 这里的 token 计算是估算值，不是模型 tokenizer 的精确值。
 * 第 15 课先建立工程结构，后续可替换为更精确 tokenizer。
 */
@ConfigurationProperties(prefix = "ai.context")
public class ContextProperties {

    /**
     * 单次模型调用允许使用的最大上下文 token。
     * 注意：这里不是模型真实最大窗口，而是业务侧主动设置的预算。
     */
    private int maxInputTokens = 8000;

    /**
     * 给模型回答预留的 token。
     * 如果不预留，输入塞太满，模型可能没有足够空间输出答案。
     */
    private int reservedOutputTokens = 1000;

    /**
     * RAG context 最多允许占用的 token。
     */
    private int maxRagContextTokens = 4000;

    /**
     * 单个 chunk 最大 token。
     * 超过后可以截断或摘要。
     */
    private int maxChunkTokens = 800;

    /**
     * 工具结果最大 token。
     */
    private int maxToolResultTokens = 1200;

    /**
     * 是否启用上下文压缩。
     */
    private boolean compressionEnabled = true;

    public int getMaxInputTokens() {
        return maxInputTokens;
    }

    public void setMaxInputTokens(int maxInputTokens) {
        this.maxInputTokens = maxInputTokens;
    }

    public int getReservedOutputTokens() {
        return reservedOutputTokens;
    }

    public void setReservedOutputTokens(int reservedOutputTokens) {
        this.reservedOutputTokens = reservedOutputTokens;
    }

    public int getMaxRagContextTokens() {
        return maxRagContextTokens;
    }

    public void setMaxRagContextTokens(int maxRagContextTokens) {
        this.maxRagContextTokens = maxRagContextTokens;
    }

    public int getMaxChunkTokens() {
        return maxChunkTokens;
    }

    public void setMaxChunkTokens(int maxChunkTokens) {
        this.maxChunkTokens = maxChunkTokens;
    }

    public int getMaxToolResultTokens() {
        return maxToolResultTokens;
    }

    public void setMaxToolResultTokens(int maxToolResultTokens) {
        this.maxToolResultTokens = maxToolResultTokens;
    }

    public boolean isCompressionEnabled() {
        return compressionEnabled;
    }

    public void setCompressionEnabled(boolean compressionEnabled) {
        this.compressionEnabled = compressionEnabled;
    }
}
```

`application.yml` 增加：

```yaml
ai:
  context:
    max-input-tokens: 8000
    reserved-output-tokens: 1000
    max-rag-context-tokens: 4000
    max-chunk-tokens: 800
    max-tool-result-tokens: 1200
    compression-enabled: true
```

启动类启用：

```java
@EnableConfigurationProperties({
        LlmProperties.class,
        RateLimitProperties.class,
        EmbeddingProperties.class,
        RagProperties.class,
        ContextProperties.class
})
```

### 代码说明

这里不追求一开始就精确计算所有模型 token，而是先建立预算机制。
