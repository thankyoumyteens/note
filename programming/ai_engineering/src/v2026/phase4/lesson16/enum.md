# 新增状态枚举

定义 Workflow 的状态和步骤，避免用字符串乱写。

Agent Workflow 应该是显式状态机，而不是“模型想干什么就干什么”。

本课先定义两个维度：

```text
WorkflowStatus：整个工单处于什么状态
WorkflowStep：当前执行到哪个步骤
```

### 代码

文件：

```text
src/main/java/com/example/aigateway/agent/model/AgentWorkflowStatus.java
```

```java
package com.example.aigateway.agent.model;

/**
 * Agent workflow 总状态。
 */
public enum AgentWorkflowStatus {
    CREATED,
    RUNNING,
    WAITING_HUMAN_REVIEW,
    COMPLETED,
    FAILED,
    STEP_LIMIT_EXCEEDED
}
```

文件：

```text
src/main/java/com/example/aigateway/agent/model/AgentWorkflowStep.java
```

```java
package com.example.aigateway.agent.model;

/**
 * Agent workflow 当前步骤。
 */
public enum AgentWorkflowStep {
    CREATED,
    PLAN,
    CHECK_ORDER,
    DRAFT_REPLY,
    HUMAN_REVIEW,
    COMPLETE,
    FAIL
}
```

### 代码说明

这里先做一个“工单处理 Agent”，所以步骤固定为：

```text
PLAN -> CHECK_ORDER -> DRAFT_REPLY -> HUMAN_REVIEW -> COMPLETE
```

后续再优化工具设计和工具可用性。
