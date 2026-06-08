# 新增结构化 AgentPlan

把第 16 课说明型 plan 升级为结构化 plan。

第 16 课：

```text
plan 是自然语言说明
```

第 17 课：

```text
plan 是结构化 DTO
```

结构化 plan 可以参与执行：

```text
intent
requiredTool
riskLevel
needHumanReview
arguments
```

### 代码

文件：

```text
src/main/java/com/example/aigateway/agent/dto/AgentPlan.java
```

```java
package com.example.aigateway.agent.dto;

import java.util.Map;

/**
 * 结构化 Agent Plan。
 *
 * 第 17 课开始，plan 不再只是说明，
 * 而是逐步参与工具选择和参数生成。
 */
public record AgentPlan(
        String intent,
        String requiredTool,
        String riskLevel,
        boolean needHumanReview,
        Map<String, Object> arguments
) {
}
```

建议在 `AgentTicket` 中新增：

```java
private AgentPlan structuredPlan;
```

对应 getter / setter 用 IDEA 生成。
