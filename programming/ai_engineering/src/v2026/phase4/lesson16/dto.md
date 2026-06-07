# 新增 DTO

定义 Controller 的请求和响应对象。

API 不应该直接暴露 `AgentTicket` 内部对象。用 DTO 可以稳定接口。

### 代码

目录：

```text
src/main/java/com/example/aigateway/agent/dto/
```

`CreateAgentTicketRequest.java`

```java
package com.example.aigateway.agent.dto;

public record CreateAgentTicketRequest(
        String title,
        String description
) {
}
```

`HumanReviewRequest.java`

```java
package com.example.aigateway.agent.dto;

public record HumanReviewRequest(
        boolean approved,
        String comment
) {
}
```

`AgentTicketResponse.java`

```java
package com.example.aigateway.agent.dto;

import com.example.aigateway.agent.model.AgentTicket;
import com.example.aigateway.agent.model.AgentWorkflowStatus;
import com.example.aigateway.agent.model.AgentWorkflowStep;
import java.util.List;
import java.util.UUID;

/**
 * Agent 工单响应 DTO。
 */
public record AgentTicketResponse(
        UUID ticketId,
        String title,
        String description,
        AgentWorkflowStatus status,
        AgentWorkflowStep currentStep,
        int stepCount,
        String plan,
        String orderCheckResult,
        String draftReply,
        String humanReviewComment,
        String summary,
        List<String> eventLogs
) {
    public static AgentTicketResponse from(AgentTicket ticket) {
        return new AgentTicketResponse(
                ticket.getId(),
                ticket.getTitle(),
                ticket.getDescription(),
                ticket.getStatus(),
                ticket.getCurrentStep(),
                ticket.getStepCount(),
                ticket.getPlan(),
                ticket.getOrderCheckResult(),
                ticket.getDraftReply(),
                ticket.getHumanReviewComment(),
                ticket.getSummary(),
                ticket.getEventLogs()
        );
    }
}
```
