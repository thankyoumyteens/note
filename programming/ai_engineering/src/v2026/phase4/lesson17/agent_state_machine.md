# 修改 AgentStateMachine

让状态机使用结构化 plan 和 ToolRegistry。

从第 17 课开始：

```text
PLAN 不再只是说明，而是生成 structuredPlan
CHECK_ORDER 不再写死，而是执行 planned tool
```

### 代码要点

修改 `runPlan`：

```java
private void runPlan(AgentTicket ticket) {
    ticket.setStatus(AgentWorkflowStatus.RUNNING);
    ticket.setCurrentStep(AgentWorkflowStep.PLAN);

    AgentPlan structuredPlan = planner.createStructuredPlan(ticket);

    ticket.setStructuredPlan(structuredPlan);
    ticket.setPlan(structuredPlan.toString());

    ticket.addLog("Structured plan created.");
}
```

修改 `runCheckOrder`：

```java
private void runCheckOrder(AgentTicket ticket) {
    ticket.setStatus(AgentWorkflowStatus.RUNNING);
    ticket.setCurrentStep(AgentWorkflowStep.CHECK_ORDER);

    ToolResult result = stepExecutor.executePlannedTool(ticket);

    String summarized = stepExecutor.summarizeToolResult(result);

    ticket.setOrderCheckResult(summarized);

    if (result.success()) {
        ticket.addLog("Planned tool executed: " + result.toolName());
    } else {
        ticket.addLog(
                "Planned tool failed: "
                        + result.errorCode()
                        + " "
                        + result.errorMessage()
        );

        /*
         * 工具失败不一定直接让 workflow FAILED。
         * 客服场景下，工具失败后可以生成草稿，要求人工核对。
         */
    }
}
```

需要 import：

```java
import com.example.aigateway.agent.dto.AgentPlan;
import com.example.aigateway.tool.dto.ToolResult;
```

### 代码说明

现在 `PLAN` 已经真正影响 `CHECK_ORDER`：

```text
PLAN.requiredTool -> 决定工具
PLAN.arguments -> 决定参数
ToolRegistry -> 执行工具
```
