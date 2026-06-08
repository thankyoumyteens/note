# 第 17 课：工具设计与 Agent 可用性优化

第 16 课已经完成了一个固定状态机 Agent：

```text
CREATED
  -> PLAN
  -> CHECK_ORDER
  -> DRAFT_REPLY
  -> HUMAN_REVIEW
  -> COMPLETE
```

第 16 课的 `PLAN` 主要是自然语言说明，用于任务分析、审计和为后续步骤提供上下文，但它不决定 Agent 的执行路径。

第 17 课开始增强这个 `PLAN`：

> 让 Agent 的 plan 从自然语言说明升级为结构化计划，并让它参与固定 workflow 中的工具选择、参数生成、风险判断和人工审核判断。

需要注意：

```text
第 17 课仍然不是动态 workflow planning。
```

也就是说，第 17 课不会让 LLM 自由决定下一步走哪个状态，主流程仍然由状态机控制：

```text
PLAN
  -> CHECK_ORDER
  -> DRAFT_REPLY
  -> HUMAN_REVIEW
  -> COMPLETE
```

第 17 课真正解决的是：

```text
在固定状态机流程中，
让结构化 plan 决定要调用哪个 tool、传什么参数、是否高风险、是否需要人工审核；
同时让工具调用变得可控、可验证、可限流、可评估。
```
