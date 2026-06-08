# 修改 AgentStepExecutor，按结构化 plan 调用工具

让工具调用路径从“固定的 checkOrder”改成“根据 plan 调用 ToolRegistry”。

Agent 不能只相信 LLM 的 plan。后端必须强制做：

```text
工具是否存在
参数是否符合要求
用户是否有权限
工具调用次数是否超限
```

### 代码

修改 `AgentStepExecutor`：

```java
package com.example.aigateway.agent.service;

import com.example.aigateway.agent.dto.AgentPlan;
import com.example.aigateway.agent.model.AgentTicket;
import com.example.aigateway.client.LlmClient;
import com.example.aigateway.context.service.ToolResultSummarizer;
import com.example.aigateway.dto.LlmCallType;
import com.example.aigateway.tool.dto.ToolDefinition;
import com.example.aigateway.tool.dto.ToolRequest;
import com.example.aigateway.tool.dto.ToolResult;
import com.example.aigateway.tool.service.ToolCallLimiter;
import com.example.aigateway.tool.service.ToolPermissionService;
import com.example.aigateway.tool.service.ToolRegistry;
import java.util.Map;
import org.springframework.stereotype.Service;

@Service
public class AgentStepExecutor {

    private final LlmClient llmClient;
    private final ToolResultSummarizer toolResultSummarizer;
    private final ToolRegistry toolRegistry;
    private final ToolPermissionService permissionService;
    private final ToolCallLimiter toolCallLimiter;

    public AgentStepExecutor(
            LlmClient llmClient,
            ToolResultSummarizer toolResultSummarizer,
            ToolRegistry toolRegistry,
            ToolPermissionService permissionService,
            ToolCallLimiter toolCallLimiter
    ) {
        this.llmClient = llmClient;
        this.toolResultSummarizer = toolResultSummarizer;
        this.toolRegistry = toolRegistry;
        this.permissionService = permissionService;
        this.toolCallLimiter = toolCallLimiter;
    }

    /**
     * 根据结构化 plan 执行工具。
     */
    public ToolResult executePlannedTool(AgentTicket ticket) {
        AgentPlan plan = ticket.getStructuredPlan();

        if (plan == null) {
            return ToolResult.failure(
                    "unknown",
                    "PLAN_MISSING",
                    "structured plan is missing"
            );
        }

        String toolName = plan.requiredTool();

        ToolDefinition definition;

        try {
            definition = toolRegistry.getRequiredDefinition(toolName);
        } catch (Exception e) {
            return ToolResult.failure(
                    toolName,
                    "TOOL_NOT_FOUND",
                    e.getMessage()
            );
        }

        if (!permissionService.canCall(definition)) {
            return ToolResult.failure(
                    toolName,
                    "TOOL_PERMISSION_DENIED",
                    "current user is not allowed to call tool: " + toolName
            );
        }

        if (!toolCallLimiter.allow(ticket)) {
            return ToolResult.failure(
                    toolName,
                    "TOOL_CALL_LIMIT_EXCEEDED",
                    "tool call limit exceeded"
            );
        }

        // 只要尝试调用工具，就计数。
        ticket.incrementToolCallCount();

        ToolRequest request = new ToolRequest(
                ticket.getId(),
                toolName,
                plan.arguments() == null ? Map.of() : plan.arguments()
        );

        return toolRegistry.execute(request);
    }

    public String draftReply(AgentTicket ticket) {
        String systemPrompt = """
                你是一个客服回复草稿生成器。

                任务：
                - 根据工单、结构化计划和工具结果生成回复草稿。
                - 如果工具结果需要人工确认，不要承诺已经退款。
                - 如果工具失败，请说明需要人工进一步核对。
                - 语气专业、简洁。
                """;

        String userPrompt = """
                工单标题：
                %s

                工单描述：
                %s

                结构化计划：
                %s

                工具结果：
                %s
                """.formatted(
                ticket.getTitle(),
                ticket.getDescription(),
                ticket.getStructuredPlan(),
                ticket.getOrderCheckResult()
        );

        return llmClient.complete(
                systemPrompt,
                userPrompt,
                LlmCallType.COMPLETE
        );
    }

    public String summarizeToolResult(ToolResult result) {
        return toolResultSummarizer.summarizeIfNeeded(
                result.toolName(),
                result.toString()
        );
    }
}
```
