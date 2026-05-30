# 添加到 WORKFLOW.md 后怎么用？

`WORKFLOW.md` 不是每天从头读一遍的文档，它的正确用法是：

> **把它当成“AI 开发操作手册 + prompt 仓库 + 行为约束来源”。**

现在它写得多，是为了先沉淀流程；真正使用时，只取其中对应场景的一小段。

## 2. 实际使用方式

你不是整篇复制，而是按场景取用。

比如你要做新功能，就打开 `WORKFLOW.md` 找：

```text
new-feature-task
Plan-Then-Act
implement-next-step
review-diff
```

然后对 AI 说：

```text
请按照 WORKFLOW.md 中的 Plan-Then-Act Tooling 流程执行。
先生成 plan，不要改代码。
```

或者：

```text
请按照 WORKFLOW.md 中的 /implement-next-step 规则，只执行下一个未完成 plan item。
完成后停止，等待我确认。
```

也就是说，`WORKFLOW.md` 的价值在于：**你不用每次重新解释规则，只要引用规则名。**

## 3. 你现在最常用的 4 个调用方式

### 场景 1：新功能开始前

```text
请阅读 WORKFLOW.md。

按照 new-feature-task 流程，把“我要实现 xxx 功能”改写成清晰任务。
只输出任务说明和计划，不要改代码。
```

### 场景 2：实现前先计划

```text
请按照 WORKFLOW.md 中的 Plan-Then-Act Tooling 执行。

先生成 plan。
不要修改文件。
计划需要包含涉及文件、修改步骤、测试计划、风险和回滚方式。
```

### 场景 3：按计划执行下一步

```text
请按照 WORKFLOW.md 中的 /implement-next-step 规则执行。

只执行下一个未完成 plan item。
完成后停止。
输出修改文件、git diff --stat、是否越界、下一步建议。
不要继续后续任务。
```

### 场景 4：实现后 review

```text
请按照 WORKFLOW.md 中的 /review-diff 规则审查当前 git diff。

重点检查：
1. 是否满足需求
2. 是否越界修改
3. 是否新增依赖
4. 是否缺少测试
5. 是否破坏已有行为
6. 是否应该回滚部分修改
```
