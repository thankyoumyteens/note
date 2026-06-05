# 新增 ContextCompressor

当单个 chunk 太长时，可以压缩成摘要再放入 prompt。

压缩不是简单截断。截断可能切掉关键信息；摘要更适合保留要点。

但压缩本身也要调用模型，有成本。所以本课只在必要时压缩。

### 代码

文件：

```text
src/main/java/com/example/aigateway/context/service/ContextCompressor.java
```

```java
package com.example.aigateway.context.service;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.context.config.ContextProperties;
import com.example.aigateway.dto.LlmCallType;
import org.springframework.stereotype.Service;

/**
 * 上下文压缩服务。
 *
 * 用于把过长文本压缩成更短的摘要。
 */
@Service
public class ContextCompressor {

    private final LlmClient llmClient;
    private final ContextProperties properties;
    private final TokenEstimator tokenEstimator;

    public ContextCompressor(
            LlmClient llmClient,
            ContextProperties properties,
            TokenEstimator tokenEstimator
    ) {
        this.llmClient = llmClient;
        this.properties = properties;
        this.tokenEstimator = tokenEstimator;
    }

    public String compressIfNeeded(String text, int maxTokens) {
        if (text == null || text.isBlank()) {
            return "";
        }

        if (!properties.isCompressionEnabled()) {
            return text;
        }

        int tokens = tokenEstimator.estimate(text);

        if (tokens <= maxTokens) {
            return text;
        }

        return compress(text, maxTokens);
    }

    private String compress(String text, int maxTokens) {
        String systemPrompt = """
                你是一个上下文压缩器。

                任务：
                - 压缩给定文本。
                - 保留和用户问答可能相关的事实。
                - 删除重复、闲聊和无关内容。
                - 不要添加原文没有的信息。
                - 输出简洁摘要。
                """;

        String userPrompt = """
                请将下面文本压缩到大约 %d token 以内：

                %s
                """.formatted(maxTokens, text);

        return llmClient.complete(
                systemPrompt,
                userPrompt,
                LlmCallType.COMPLETE
        );
    }
}
```

### 代码说明

这里复用 `LlmClient`，不绕过 AI Gateway。
