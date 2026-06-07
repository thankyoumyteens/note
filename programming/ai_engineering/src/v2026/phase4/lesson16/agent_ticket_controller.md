# 新增 AgentTicketController

暴露 Agent Workflow API。

Agent Workflow 应该能被外部系统驱动：

```text
创建工单
推进一步
查看状态
提交人工审核
```

### 代码

文件：

```text
src/main/java/com/example/aigateway/agent/controller/AgentTicketController.java
```

```java
package com.example.aigateway.agent.controller;

import com.example.aigateway.agent.dto.AgentTicketResponse;
import com.example.aigateway.agent.dto.CreateAgentTicketRequest;
import com.example.aigateway.agent.dto.HumanReviewRequest;
import com.example.aigateway.agent.service.AgentWorkflowService;
import java.util.UUID;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/agent/tickets")
public class AgentTicketController {

    private final AgentWorkflowService workflowService;

    public AgentTicketController(AgentWorkflowService workflowService) {
        this.workflowService = workflowService;
    }

    @PostMapping
    public AgentTicketResponse create(@RequestBody CreateAgentTicketRequest request) {
        return AgentTicketResponse.from(
                workflowService.create(request)
        );
    }

    @PostMapping("/{ticketId}/run")
    public AgentTicketResponse run(@PathVariable UUID ticketId) {
        return AgentTicketResponse.from(
                workflowService.run(ticketId)
        );
    }

    @GetMapping("/{ticketId}")
    public AgentTicketResponse get(@PathVariable UUID ticketId) {
        return AgentTicketResponse.from(
                workflowService.get(ticketId)
        );
    }

    @PostMapping("/{ticketId}/human-review")
    public AgentTicketResponse humanReview(
            @PathVariable UUID ticketId,
            @RequestBody HumanReviewRequest request
    ) {
        return AgentTicketResponse.from(
                workflowService.humanReview(ticketId, request)
        );
    }
}
```
