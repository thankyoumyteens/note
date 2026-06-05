# 新增 ToolResultSummarizer

为后续 Agent 和复杂工具调用准备工具结果摘要能力。

工具返回可能很长，例如：

```text
订单详情 JSON
数据库查询结果
搜索结果列表
日志片段
网页内容
```

不能全部塞进 prompt。

本课先新增服务，不强行接入 Agent。

### 代码

文件：

```text
src/main/java/com/example/aigateway/context/service/ToolResultSummarizer.java
```

```java
package com.example.aigateway.context.service;

import com.example.aigateway.client.LlmClient;
import com.example.aigateway.context.config.ContextProperties;
import com.example.aigateway.dto.LlmCallType;
import org.springframework.stereotype.Service;

/**
 * 工具结果摘要服务。
 *
 * 第 15 课先提供能力。
 * 第 16 / 17 课 Agent 和工具体系增强时再深入使用。
 */
@Service
public class ToolResultSummarizer {

    private final LlmClient llmClient;
    private final ContextProperties properties;
    private final TokenEstimator tokenEstimator;

    public ToolResultSummarizer(
            LlmClient llmClient,
            ContextProperties properties,
            TokenEstimator tokenEstimator
    ) {
        this.llmClient = llmClient;
        this.properties = properties;
        this.tokenEstimator = tokenEstimator;
    }

    public String summarizeIfNeeded(String toolName, String toolResult) {
        if (toolResult == null || toolResult.isBlank()) {
            return "";
        }

        int tokens = tokenEstimator.estimate(toolResult);

        if (tokens <= properties.getMaxToolResultTokens()) {
            return toolResult;
        }

        String systemPrompt = """
                你是一个工具结果摘要器。

                任务：
                - 压缩工具返回结果。
                - 保留和用户任务有关的字段。
                - 保留错误信息、状态码、关键 ID、金额、时间、结论。
                - 删除重复和无关字段。
                - 不要编造工具结果中没有的信息。
                """;

        String userPrompt = """
                工具名称：
                %s

                工具原始结果：
                %s
                """.formatted(toolName, toolResult);

        return llmClient.complete(
                systemPrompt,
                userPrompt,
                LlmCallType.COMPLETE
        );
    }
}
```

### 代码说明

这一步是为第 16 / 17 课铺垫。
