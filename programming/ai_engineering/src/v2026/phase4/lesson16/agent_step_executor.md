# 新增 AgentStepExecutor

执行具体步骤，例如检查订单、生成回复草稿。

Agent step 要有限制、有边界。

本课先模拟一个订单检查工具，不接入真实订单系统。

### 代码

文件：

```text
src/main/java/com/example/aigateway/agent/service/AgentStepExecutor.java
```

```java
package com.example.aigateway.agent.service;

import com.example.aigateway.agent.model.AgentTicket;
import com.example.aigateway.client.LlmClient;
import com.example.aigateway.context.service.ToolResultSummarizer;
import com.example.aigateway.dto.LlmCallType;
import org.springframework.stereotype.Service;

/**
 * Agent 步骤执行器。
 *
 * 第 16 课先使用简单模拟工具。
 * 第 17 课再正式优化工具设计、工具描述、工具 eval。
 */
@Service
public class AgentStepExecutor {

    private final LlmClient llmClient;
    private final ToolResultSummarizer toolResultSummarizer;

    public AgentStepExecutor(
            LlmClient llmClient,
            ToolResultSummarizer toolResultSummarizer
    ) {
        this.llmClient = llmClient;
        this.toolResultSummarizer = toolResultSummarizer;
    }

    public String checkOrder(AgentTicket ticket) {
        /*
         * 模拟订单查询工具。
         * 后续第 17 课可替换为真实 Tool Registry。
         */
        String rawToolResult = """
                {
                  "orderId": "ORDER-1001",
                  "status": "REFUND_REQUESTED",
                  "refundStatus": "PENDING_REVIEW",
                  "risk": "POSSIBLE_DUPLICATE_REFUND",
                  "message": "订单存在退款申请，但需要人工确认是否重复退款。"
                }
                """;

        return toolResultSummarizer.summarizeIfNeeded(
                "checkOrder",
                rawToolResult
        );
    }

    public String draftReply(AgentTicket ticket) {
        String systemPrompt = """
                你是一个客服回复草稿生成器。

                任务：
                - 根据工单、处理计划和订单检查结果生成回复草稿。
                - 如果订单结果需要人工确认，不要承诺已经退款。
                - 语气专业、简洁。
                """;

        String userPrompt = """
                工单标题：
                %s

                工单描述：
                %s

                处理计划：
                %s

                订单检查结果：
                %s
                """.formatted(
                ticket.getTitle(),
                ticket.getDescription(),
                ticket.getPlan(),
                ticket.getOrderCheckResult()
        );

        return llmClient.complete(
                systemPrompt,
                userPrompt,
                LlmCallType.COMPLETE
        );
    }
}
```

### 代码说明

这里复用了第 15 课的：

```text
ToolResultSummarizer
```

说明 Context Engineering 开始服务于 Agent。
