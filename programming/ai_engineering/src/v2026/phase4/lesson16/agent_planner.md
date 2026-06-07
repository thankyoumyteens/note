# 新增 AgentPlanner

让 LLM 生成一个处理计划，但不直接执行所有动作。

Agent 不是“让模型一次性搞定全部”。更可靠的方式是：

```text
先规划
再按状态机执行
每一步可审计、可停止、可恢复
```

### 代码

文件：

```text
src/main/java/com/example/aigateway/agent/service/AgentPlanner.java
```

```java
package com.example.aigateway.agent.service;

import com.example.aigateway.agent.model.AgentTicket;
import com.example.aigateway.client.LlmClient;
import com.example.aigateway.dto.LlmCallType;
import org.springframework.stereotype.Service;

/**
 * Agent 规划器。
 *
 * 只负责生成计划，不负责执行工具。
 */
@Service
public class AgentPlanner {

    private final LlmClient llmClient;

    public AgentPlanner(LlmClient llmClient) {
        this.llmClient = llmClient;
    }

    public String createPlan(AgentTicket ticket) {
        String systemPrompt = """
                你是一个企业客服工单处理 Agent 的规划器。

                任务：
                - 根据工单标题和描述生成处理计划。
                - 只生成计划，不要编造工具结果。
                - 不要直接回复客户。
                - 计划应该简洁，最多 3 步。
                """;

        String userPrompt = """
                工单标题：
                %s

                工单描述：
                %s
                """.formatted(ticket.getTitle(), ticket.getDescription());

        return llmClient.complete(
                systemPrompt,
                userPrompt,
                LlmCallType.COMPLETE
        );
    }
}
```

### 代码说明

本课只是 workflow 入门，所以计划是自然语言文本。

后续再做更严格的工具选择和参数结构化。

本课的 PLAN 只是帮助你理解：

```
Agent 先分析任务，再进入后续固定流程
```

但它不决定下一步走哪个工具。

到了第 17 课，PLAN 会开始升级为更有执行意义的东西，例如：

```json
{
  "intent": "REFUND_STATUS_CHECK",
  "requiredTools": ["checkOrder"],
  "riskLevel": "HIGH",
  "needHumanReview": true,
  "nextAction": "CHECK_ORDER",
  "arguments": {
    "orderId": "ORDER-1001"
  }
}
```

也就是从自然语言说明，升级成：

```
结构化计划
工具选择
参数生成
权限检查
工具调用次数限制
工具调用 eval
```

这时 plan 才开始真正影响 Agent 执行。
