# 第 11C 课：使用 spec-workflow-mcp + TDD Skill 的组合实践

前面你已经分别学过：

```text
Spec Workflow：
管理需求范围、design、tasks、approval、进度。

TDD Skill：
管理 Red / Green / Refactor 代码行为。
```

第 11C 的目标是把它们组合起来：

```text
spec-workflow-mcp 管 feature 范围和任务
TDD Skill 管测试驱动实现
```

也就是：

```text
先用 spec-workflow-mcp 明确做什么、不做什么
再用 tdd-red / tdd-green / tdd-refactor 完成代码行为
```

## 本课分两步：

```text
第一步：创建组合 Skill
第二步：使用组合 Skill 实战一个小功能
```

组合 Skill 名称建议：

```text
spec-tdd-cycle
```

它负责把这两个东西组合起来：

```text
spec-workflow-mcp：管理 feature、requirements、design、tasks
TDD Skills：管理 Red / Green / Refactor
```

最终你日常不应该再写超长 prompt，而是说：

```text
使用 spec-tdd-cycle skill。
功能：PATCH /api/documents/{id}/title。
本轮只执行第 0 轮状态检查和计划，不修改文件。
```

后续继续时只说：

```text
继续。按 spec-tdd-cycle skill 只执行下一轮唯一 task。
```
