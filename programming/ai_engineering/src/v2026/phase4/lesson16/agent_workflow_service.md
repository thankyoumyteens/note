# 新增 AgentWorkflowService

封装 Controller 和状态机之间的业务逻辑。

Controller 不应该直接操作状态机和 repository。

### 代码

文件：

```text
src/main/java/com/example/aigateway/agent/service/AgentWorkflowService.java
```

```java
package com.example.aigateway.agent.service;

import com.example.aigateway.agent.dto.CreateAgentTicketRequest;
import com.example.aigateway.agent.dto.HumanReviewRequest;
import com.example.aigateway.agent.model.AgentTicket;
import com.example.aigateway.agent.model.AgentWorkflowStatus;
import com.example.aigateway.agent.model.AgentWorkflowStep;
import com.example.aigateway.agent.repository.AgentTicketRepository;
import java.util.UUID;
import org.springframework.stereotype.Service;

@Service
public class AgentWorkflowService {

    private final AgentTicketRepository repository;
    private final AgentStateMachine stateMachine;

    public AgentWorkflowService(
            AgentTicketRepository repository,
            AgentStateMachine stateMachine
    ) {
        this.repository = repository;
        this.stateMachine = stateMachine;
    }

    public AgentTicket create(CreateAgentTicketRequest request) {
        if (request == null || request.title() == null || request.title().isBlank()) {
            throw new IllegalArgumentException("title cannot be empty");
        }

        if (request.description() == null || request.description().isBlank()) {
            throw new IllegalArgumentException("description cannot be empty");
        }

        AgentTicket ticket = AgentTicket.create(
                request.title(),
                request.description()
        );

        return repository.save(ticket);
    }

    public AgentTicket run(UUID ticketId) {
        AgentTicket ticket = getRequired(ticketId);

        if (ticket.getStatus() == AgentWorkflowStatus.COMPLETED) {
            return ticket;
        }

        if (ticket.getStatus() == AgentWorkflowStatus.WAITING_HUMAN_REVIEW) {
            return ticket;
        }

        stateMachine.runNext(ticket);
        return repository.save(ticket);
    }

    public AgentTicket get(UUID ticketId) {
        return getRequired(ticketId);
    }

    public AgentTicket humanReview(UUID ticketId, HumanReviewRequest request) {
        AgentTicket ticket = getRequired(ticketId);

        if (ticket.getStatus() != AgentWorkflowStatus.WAITING_HUMAN_REVIEW) {
            throw new IllegalStateException("ticket is not waiting for human review");
        }

        ticket.setHumanReviewComment(request.comment());
        ticket.addLog("Human review submitted. approved=" + request.approved());

        if (request.approved()) {
            ticket.setCurrentStep(AgentWorkflowStep.HUMAN_REVIEW);
            stateMachine.runNext(ticket);
        } else {
            ticket.setStatus(AgentWorkflowStatus.FAILED);
            ticket.setCurrentStep(AgentWorkflowStep.FAIL);
            ticket.setSummary("Workflow rejected by human reviewer.");
            ticket.addLog("Workflow rejected by human.");
        }

        return repository.save(ticket);
    }

    private AgentTicket getRequired(UUID ticketId) {
        return repository.findById(ticketId)
                .orElseThrow(() -> new IllegalArgumentException("ticket not found: " + ticketId));
    }
}
```

### 代码说明

`run(...)` 一次只执行一步。

所以如果想从 CREATED 跑到 HUMAN_REVIEW，需要调用多次：

```text
POST /run
POST /run
POST /run
POST /run
```

这有意为之：便于观察每一步状态变化。
