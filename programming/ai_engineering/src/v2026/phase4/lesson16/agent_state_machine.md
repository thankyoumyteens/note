# 新增 AgentStateMachine

用状态机控制 workflow 走向。

状态机的好处：

```text
可预测
可测试
可恢复
可审计
不会无限循环
```

### 代码

文件：

```text
src/main/java/com/example/aigateway/agent/service/AgentStateMachine.java
```

```java
package com.example.aigateway.agent.service;

import com.example.aigateway.agent.config.AgentProperties;
import com.example.aigateway.agent.model.AgentTicket;
import com.example.aigateway.agent.model.AgentWorkflowStatus;
import com.example.aigateway.agent.model.AgentWorkflowStep;
import org.springframework.stereotype.Service;

/**
 * Agent 状态机。
 *
 * 负责推进 workflow。
 */
@Service
public class AgentStateMachine {

    private final AgentProperties properties;
    private final AgentPlanner planner;
    private final AgentStepExecutor stepExecutor;

    public AgentStateMachine(
            AgentProperties properties,
            AgentPlanner planner,
            AgentStepExecutor stepExecutor
    ) {
        this.properties = properties;
        this.planner = planner;
        this.stepExecutor = stepExecutor;
    }

    public void runNext(AgentTicket ticket) {
        if (ticket.getStepCount() >= properties.getMaxSteps()) {
            ticket.setStatus(AgentWorkflowStatus.STEP_LIMIT_EXCEEDED);
            ticket.setCurrentStep(AgentWorkflowStep.FAIL);
            ticket.addLog("Agent step limit exceeded.");
            return;
        }

        ticket.incrementStepCount();

        try {
            switch (ticket.getCurrentStep()) {
                case CREATED -> runPlan(ticket);
                case PLAN -> runCheckOrder(ticket);
                case CHECK_ORDER -> runDraftReply(ticket);
                case DRAFT_REPLY -> waitHumanReview(ticket);
                case HUMAN_REVIEW -> complete(ticket);
                default -> {
                    ticket.setStatus(AgentWorkflowStatus.FAILED);
                    ticket.setCurrentStep(AgentWorkflowStep.FAIL);
                    ticket.addLog("Invalid workflow step: " + ticket.getCurrentStep());
                }
            }
        } catch (Exception e) {
            ticket.setStatus(AgentWorkflowStatus.FAILED);
            ticket.setCurrentStep(AgentWorkflowStep.FAIL);
            ticket.addLog("Agent step failed: " + e.getMessage());
        }
    }

    private void runPlan(AgentTicket ticket) {
        ticket.setStatus(AgentWorkflowStatus.RUNNING);
        ticket.setCurrentStep(AgentWorkflowStep.PLAN);

        String plan = planner.createPlan(ticket);
        ticket.setPlan(plan);
        ticket.addLog("Plan created.");
    }

    private void runCheckOrder(AgentTicket ticket) {
        ticket.setStatus(AgentWorkflowStatus.RUNNING);
        ticket.setCurrentStep(AgentWorkflowStep.CHECK_ORDER);

        String result = stepExecutor.checkOrder(ticket);
        ticket.setOrderCheckResult(result);
        ticket.addLog("Order checked.");
    }

    private void runDraftReply(AgentTicket ticket) {
        ticket.setStatus(AgentWorkflowStatus.RUNNING);
        ticket.setCurrentStep(AgentWorkflowStep.DRAFT_REPLY);

        String draftReply = stepExecutor.draftReply(ticket);
        ticket.setDraftReply(draftReply);
        ticket.addLog("Draft reply generated.");
    }

    private void waitHumanReview(AgentTicket ticket) {
        ticket.setStatus(AgentWorkflowStatus.WAITING_HUMAN_REVIEW);
        ticket.setCurrentStep(AgentWorkflowStep.HUMAN_REVIEW);
        ticket.addLog("Waiting for human review.");
    }

    private void complete(AgentTicket ticket) {
        ticket.setStatus(AgentWorkflowStatus.COMPLETED);
        ticket.setCurrentStep(AgentWorkflowStep.COMPLETE);
        ticket.setSummary("Workflow completed with human review.");
        ticket.addLog("Workflow completed.");
    }
}
```

### 代码说明

`runNext(...)` 一次只推进一步。

这样比一次性 while 循环更安全，也更容易调试。
