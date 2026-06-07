# 新增 AgentTicket

定义一个 Agent 要处理的工单对象。

Agent 不能只处理一段 prompt。企业系统里 Agent 通常围绕业务对象运行：

```text
工单
订单
合同
审批单
客户请求
```

本课使用工单作为最小业务对象。

### 代码

文件：

```text
src/main/java/com/example/aigateway/agent/model/AgentTicket.java
```

```java
package com.example.aigateway.agent.model;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * Agent 工单对象。
 *
 * 第 16 课先用内存存储。
 * 后续可替换为数据库表。
 */
public class AgentTicket {

    private UUID id;
    private String title;
    private String description;

    private AgentWorkflowStatus status;
    private AgentWorkflowStep currentStep;

    private int stepCount;
    private String plan;
    private String orderCheckResult;
    private String draftReply;
    private String humanReviewComment;
    private String summary;

    private List<String> eventLogs = new ArrayList<>();

    private Instant createdAt;
    private Instant updatedAt;

    public static AgentTicket create(String title, String description) {
        AgentTicket ticket = new AgentTicket();

        ticket.id = UUID.randomUUID();
        ticket.title = title;
        ticket.description = description;
        ticket.status = AgentWorkflowStatus.CREATED;
        ticket.currentStep = AgentWorkflowStep.CREATED;
        ticket.stepCount = 0;
        ticket.createdAt = Instant.now();
        ticket.updatedAt = Instant.now();
        ticket.addLog("Ticket created.");

        return ticket;
    }

    public void addLog(String log) {
        eventLogs.add(Instant.now() + " " + log);
        updatedAt = Instant.now();
    }

    public void incrementStepCount() {
        stepCount++;
        updatedAt = Instant.now();
    }

    // 为了节省篇幅，下面 getter / setter 可以用 IDEA Generate 生成。
    // 如果你项目使用 Lombok，也可以用 @Getter / @Setter。
}
```

### 代码说明

本课先用普通 Java class，不强行引入 JPA。

字段含义：

```text
plan：LLM 拆解出的处理计划
orderCheckResult：订单检查结果
draftReply：给客户的回复草稿
humanReviewComment：人工审核意见
summary：最终总结
eventLogs：workflow 事件日志
```
