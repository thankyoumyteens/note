# 第 12 课：Hooks 自动化：测试、格式化、提醒

你前面已经学会了用 prompt / skill / MCP 约束 AI：

```text
使用 tdd-red skill
使用 tdd-green skill
使用 tdd-refactor skill
使用 spec-tdd-cycle skill
每次只执行一个 task
```

但这些都依赖 AI “记得遵守”。

Hooks 的作用是：**把某些提醒、检查、拦截变成工具层面的自动动作。**

简单说：

```text
Skill：告诉 AI 应该怎么做
Hook：在某些时机自动提醒 / 检查 / 阻止
```

例如：

```text
AI 修改 Java 代码后，提醒它运行 mvn test
AI 试图执行 git commit 时，提醒或阻止
AI 试图运行 mvn spring-boot:run 时，提醒它不要长期占用端口
AI 修改 pom.xml 时，提醒必须说明是否新增依赖
```

## Hook 和 Skill 的区别

| 对比     | Skill                          | Hook                         |
| -------- | ------------------------------ | ---------------------------- |
| 作用     | 规定流程                       | 自动触发动作                 |
| 触发方式 | 用户或 AI 选择使用             | 工具在特定事件时触发         |
| 适合内容 | TDD、Spec+TDD、Review、Handoff | 测试提醒、命令拦截、安全检查 |
| 例子     | `tdd-red`                      | 修改代码后提醒运行测试       |
| 风险     | AI 可能不用                    | 配太多会烦、会误拦截         |

一句话：

```text
Skill 管“怎么做”
Hook 管“什么时候自动提醒/检查/拦截”
```

## Hook 事件怎么理解

| Event                            | 适合做什么                                                              |
| -------------------------------- | ----------------------------------------------------------------------- |
| `PreToolUse`                     | 工具执行前检查，例如拦截 `git commit`、`git add`、`mvn spring-boot:run` |
| `PermissionRequest`              | 工具请求权限时做额外判断                                                |
| `PostToolUse`                    | 工具执行后提醒，例如修改 Java 文件后提醒运行 `mvn test`                 |
| `UserPromptSubmit`               | 用户提交 prompt 后检查是否有明显问题                                    |
| `SessionStart`                   | 会话开始时提示读取项目规则或显示项目注意事项                            |
| `Stop`                           | AI 本轮结束前提醒输出测试结果、`git status`、`git diff --stat`          |
| `PreCompact` / `PostCompact`     | 上下文压缩前后保存或提醒关键信息                                        |
| `SubagentStart` / `SubagentStop` | 子 agent 启动/结束时提示边界或要求汇报                                  |

本课只建议先重点看：

```text
PreToolUse
PostToolUse
Stop
```

建议先设计 3 类：

### A. PreToolUse：高风险命令拦截或提醒

适合检查：

```text
git add
git commit
mvn spring-boot:run
mvn clean install
修改 pom.xml 前后的风险
```

其中最重要的是：

```text
不要让 AI 自动 git add / git commit。
不要让 AI 长时间运行 mvn spring-boot:run 占用端口。
```

### B. PostToolUse：修改后提醒测试

适合检查：

```text
如果修改了 src/main/java 或 src/test/java
提醒运行 mvn test
```

当前先做“提醒”，不要自动运行。

### C. Stop：回合结束前提醒汇报

适合在 AI 回合结束前提醒：

```text
本轮修改了什么
是否运行测试
测试结果是什么
git status 摘要
git diff --stat 摘要
是否有越界修改
```
