# 因不可抗力中断后让 AI 继续执行任务

重新打开 Codex / Claude Code 后，不要直接说“继续”。应该先让它做 **resume check**，只恢复现场，不执行任务。

可以这样说：

```text
恢复当前工作流。

请使用 spec-tdd-cycle skill。
先只做 resume check，不要修改任何文件，不要执行任何 task。

请读取：
1. AGENTS.md
2. CLAUDE.md
3. WORKFLOW.md
4. skills/spec-tdd-cycle/SKILL.md
5. skills/tdd-red/SKILL.md
6. skills/tdd-green/SKILL.md
7. skills/tdd-refactor/SKILL.md
8. 当前 git status
9. 当前 git diff
10. spec-workflow-mcp 中当前 active feature 的 requirements / design / tasks / task 状态

请判断：
1. 当前 active feature 是什么
2. 当前 workflow phase 是什么
3. 已完成哪些 tasks
4. 当前第一个未完成 task 是什么
5. 工作区是否有未提交修改
6. 未提交修改是否属于当前 task
7. MCP task 状态是否和实际文件修改一致
8. 是否存在越界修改
9. 推荐下一步唯一 action 是什么

输出后停止，等待我确认。
```

---

## AI 检查完后，你怎么继续

确认它判断正确后，说：

```text
继续。只执行当前第一个未完成 task，完成后停止，等待我确认。
```

或者更明确：

```text
继续。只执行当前 document-title-update 功能的下一步唯一 action。不要执行后续 task。完成后输出 git status、git diff --stat、测试结果和 task 状态，然后停止。
```

---

## 不要这样说

不要只说：

```text
继续
```

因为中断后 AI 可能不知道：

```text
feature 创建了吗？
requirements 完成了吗？
design 完成了吗？
Red 测试写了吗？
Green 实现做到一半了吗？
MCP task 状态是否准确？
git diff 是否包含上次未完成修改？
```

“继续”太模糊，容易导致它跳步或重复执行。

---

## 建议写进 `spec-tdd-cycle/SKILL.md`

把恢复逻辑写成真实项目语言：

```markdown
## Resume after interruption

Use this section when the session was interrupted, the machine restarted, context was lost, or the user asks to continue an existing workflow.

Rules:

1. Do not continue execution immediately.
2. Do not modify files during resume check.
3. Do not mark tasks as completed during resume check.
4. Read project instructions, workflow index, this skill, related TDD skills, git status, git diff, and current spec-workflow-mcp feature state.
5. Identify the active feature.
6. Identify the current workflow phase.
7. Identify completed tasks.
8. Identify the first unfinished task.
9. Check whether uncommitted changes match the current task.
10. Check whether MCP task state matches actual file changes.
11. Report inconsistencies.
12. Wait for user confirmation before executing the next task.

Output format:

- Active feature:
- Current workflow phase:
- Completed tasks:
- First unfinished task:
- Uncommitted changes:
- Do uncommitted changes match the current task:
- MCP task state:
- Inconsistencies:
- Recommended next action:
- Waiting for user confirmation.
```

日常恢复用这一句就够：

```text
使用 spec-tdd-cycle skill 的 resume after interruption 流程。先只做状态检查，不要修改文件，不要执行 task。找出当前第一个未完成 task，并等待我确认。
```

---

## 更通用：单独做一个恢复 Skill

真实项目里，我更建议你做一个通用 Skill：

```text
skills/resume-workflow/SKILL.md
```

它不绑定 TDD，也不绑定 spec-workflow，只负责恢复现场。

以后你可以说：

```text
使用 resume-workflow skill，恢复当前 feature 的工作流。先只做状态检查，不要修改文件。
```

它应该检查：

```text
git status
git diff
当前 feature 状态
当前 task 状态
测试状态
未完成工作
下一步唯一 action
```

这样比把恢复逻辑塞进每个 Skill 更通用。
