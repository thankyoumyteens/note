# Commands / Skills 分别是什么

## Commands

可以理解为：

```text
一次性工作流入口
```

适合做成 command 的东西通常是：

```text
/new-feature-task
/review-diff
/write-handoff
/plan
/implement-step
```

它们像“快捷命令”，用于触发一段固定流程。

例如：

```text
/new-feature-task 文档保存功能
```

期望输出：

```text
目标
背景
输入
输出
限制
验收标准
接口设计
测试计划
风险点
后续任务拆分
```

## Skills

可以理解为：

```text
可复用能力包
```

适合做成 skill 的东西通常更完整，可能包含：

```text
说明文件
模板
检查清单
示例
脚本
约束规则
```

例如：

```text
feature-task-skill
review-diff-skill
handoff-skill
```

它比 command 更像“能力模块”。

## 本课只做设计，不做完整实现

第 5A 课不要急着真的创建 `.claude/commands/` 或 `skills/` 目录，除非你明确想让 Claude Code 只创建设计稿。

本课建议只创建或更新：

```text
WORKFLOW.md
```

或者让 Claude Code 只在对话中输出设计方案。

如果要落文件，建议只让它写入：

```text
WORKFLOW.md 的 Prompt Tooling 章节
```

不要让它现在就创建复杂目录：

```text
.claude/
skills/
scripts/
hooks/
```

这些后面的课会系统做。
