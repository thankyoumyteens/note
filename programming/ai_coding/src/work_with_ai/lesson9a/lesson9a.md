# 第 9A 课：Spec Workflow 工具化：spec-workflow-mcp

第 8～9 课你已经手写并使用了：

```text
specs/document-query/
  requirements.md
  design.md
  tasks.md
  test.md
```

你也发现了手写 Spec 的真实痛点：

```text
AI 可能最后统一勾选 tasks.md
task 状态可能和真实代码进度不同步
审批、反馈、修改记录都靠人手动维护
```

第 9A 课要学习：

```text
@pimzino/spec-workflow-mcp 这类工具到底解决什么问题。
```

本课重点不是马上用它做新功能，而是：

```text
安装 / 配置 / 观察 / 记录
理解它的 spec 生命周期
确认它和手写 spec 的区别
明确工具权限和边界
```

## 这个工具解决什么问题

`spec-workflow-mcp` 是一个用于结构化规格驱动开发的 MCP Server，官方描述包含 Requirements → Design → Tasks 的顺序工作流、实时 Dashboard、VS Code 扩展、审批流程、任务进度跟踪和实现日志等能力。

它主要解决这些问题：

| 手写 Spec 的问题      | spec-workflow-mcp 的价值 |
| --------------------- | ------------------------ |
| spec 文件结构靠人维护 | 提供结构化 spec workflow |
| tasks 状态靠手动勾选  | 提供任务进度跟踪         |
| 审批靠聊天记录        | 提供 approval workflow   |
| 进度不直观            | 提供实时 Web Dashboard   |
| IDE 内查看不方便      | 提供 VS Code 扩展侧边栏  |
| 实现记录分散          | 提供 implementation logs |

它不是替你写代码的魔法工具，而是把：

```text
requirements → design → tasks → approval → implementation tracking
```

变成更稳定的工具流程。
