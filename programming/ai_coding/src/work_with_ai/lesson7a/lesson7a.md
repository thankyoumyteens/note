# 第 7A 课：Plan-Then-Act 工具化

Codex / Claude Code 都可能自带 Plan-Then-Act 行为。

但问题是：

```text
它们会 plan，不代表它们会真正小步实现。
```

这说明：

```text
Plan-Then-Act 不能只停留在“让 AI 先计划”。
还要工具化成“每次只执行下一个未完成任务”。
```

也就是说，真正的工作流应该是：

```text
1. AI 生成 plan
2. 人类审查 plan
3. AI 只执行下一个未完成 plan item
4. AI 输出 diff 摘要
5. 人类检查 git diff / 测试结果
6. 人类确认继续
7. AI 再执行下一个 plan item
```

这才是你后续要复用的 Plan-Then-Act。

第 7A 课的目标就是把这个规则写进 `WORKFLOW.md`。
