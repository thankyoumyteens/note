# 修改 AgentPlanner，输出结构化 plan

让 LLM 生成 JSON plan，并用 Jackson 解析成 `AgentPlan`。

这是第 4～5 课结构化输出能力在 Agent 中的应用。

先用 prompt 约束 JSON + Jackson 解析。不要在本课引入更复杂规划器。

### 代码

修改：

```text
src/main/java/com/example/aigateway/agent/service/AgentPlanner.java
```

```java
package com.example.aigateway.agent.service;

import com.example.aigateway.agent.dto.AgentPlan;
import com.example.aigateway.agent.model.AgentTicket;
import com.example.aigateway.client.LlmClient;
import com.example.aigateway.dto.LlmCallType;
import com.example.aigateway.tool.dto.ToolDefinition;
import com.example.aigateway.tool.service.ToolRegistry;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.List;
import org.springframework.stereotype.Service;

/**
 * Agent 规划器。
 *
 * 第 17 课开始输出结构化 plan。
 */
@Service
public class AgentPlanner {

    private final LlmClient llmClient;
    private final ToolRegistry toolRegistry;
    private final ObjectMapper objectMapper;

    public AgentPlanner(
            LlmClient llmClient,
            ToolRegistry toolRegistry,
            ObjectMapper objectMapper
    ) {
        this.llmClient = llmClient;
        this.toolRegistry = toolRegistry;
        this.objectMapper = objectMapper;
    }

    public AgentPlan createStructuredPlan(AgentTicket ticket) {
        List<ToolDefinition> tools = toolRegistry.listTools();

        String systemPrompt = """
                你是一个企业客服 Agent 的结构化规划器。

                任务：
                - 根据工单内容，从可用工具中选择一个最合适的工具。
                - 生成工具参数。
                - 判断风险等级。
                - 判断是否需要人工审核。

                只能输出 JSON，不要输出解释。

                JSON 格式：
                {
                  "intent": "REFUND_STATUS_CHECK",
                  "requiredTool": "checkOrder",
                  "riskLevel": "LOW|MEDIUM|HIGH",
                  "needHumanReview": true,
                  "arguments": {
                    "orderId": "ORDER-1001"
                  }
                }

                规则：
                - requiredTool 必须来自可用工具列表。
                - 如果工单中没有订单号，arguments.orderId 为空字符串。
                - 不要编造订单号。
                """;

        String userPrompt = """
                可用工具：
                %s

                工单标题：
                %s

                工单描述：
                %s
                """.formatted(
                tools,
                ticket.getTitle(),
                ticket.getDescription()
        );

        String json = llmClient.complete(
                systemPrompt,
                userPrompt,
                LlmCallType.COMPLETE
        );

        try {
            return objectMapper.readValue(json, AgentPlan.class);
        } catch (Exception e) {
            throw new IllegalStateException("Failed to parse AgentPlan: " + json, e);
        }
    }
}
```

### 代码说明

这里让 plan 真正开始影响执行：

```text
requiredTool 决定调用哪个工具
arguments 决定传什么参数
riskLevel / needHumanReview 决定后续是否人工审核
```

如果你遇到大模型返回的 JSON 格式错误的问题，复用第 5 课 JSON 修复能力即可。
