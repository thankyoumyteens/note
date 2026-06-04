# 创建组合 Skill

## 目标

创建：

```text
skills/spec-tdd-cycle/SKILL.md
```

可选同步到工具可发现目录：

```text
.agents/skills/spec-tdd-cycle/SKILL.md
.claude/skills/spec-tdd-cycle/SKILL.md
```

这个 Skill 的作用是：

```text
把 spec-workflow-mcp + tdd-red / tdd-green / tdd-refactor 串起来
并强制 one-task-at-a-time gate
```

---

## 给 Claude Code / Codex 的 Prompt

把下面这段发给 AI：

```text
目标：
创建 spec-tdd-cycle 组合 Skill。

本课目标：
创建一个组合 Skill，用于把 spec-workflow-mcp 和 TDD Skills 组合起来。
本轮只创建 Skill，不实现业务功能。

请先读取：
1. AGENTS.md
2. CLAUDE.md
3. WORKFLOW.md
4. skills/tdd-red/SKILL.md
5. skills/tdd-green/SKILL.md
6. skills/tdd-refactor/SKILL.md
7. 当前 git status

需要创建：
1. skills/spec-tdd-cycle/SKILL.md

需要同步到：
1. .agents/skills/spec-tdd-cycle/SKILL.md
2. .claude/skills/spec-tdd-cycle/SKILL.md

Skill 目标：
spec-tdd-cycle 用于中等复杂度功能开发。
它必须组合使用：
1. spec-workflow-mcp
2. tdd-red skill
3. tdd-green skill
4. tdd-refactor skill

Skill 必须强制 one-task-at-a-time gate：
1. 每次只执行一个 task。
2. 完成当前 task 后必须停止。
3. 不允许继续执行下一个 task。
4. 不允许最后统一批量标记 MCP tasks 完成。
5. 必须等待用户明确回复“继续”后，才允许执行下一轮。

SKILL.md 必须包含：
1. YAML frontmatter：
   - name: spec-tdd-cycle
   - description: Use this skill when a feature requires spec-workflow-mcp for requirements/design/tasks and TDD skills for Red/Green/Refactor, one task at a time.
2. Purpose
3. When to use
4. When not to use
5. Inputs
6. Required tools
7. Execution rounds
8. One-task-at-a-time gate
9. Output format for each round
10. Hard rules
11. Completion checklist
12. Common mistakes to avoid

Execution rounds 必须包含：
第 0 轮：状态检查与计划输出，不修改文件。
第 1 轮：只创建或确认 MCP feature。
第 2 轮：只完成 requirements。
第 3 轮：只完成 design。
第 4 轮：只完成 tasks。
第 5 轮：使用 tdd-red，只写失败测试。
第 6 轮：使用 tdd-green，写最小实现。
第 7 轮：使用 tdd-refactor，评估并小步重构。
第 8 轮：最终验收汇总。

Hard rules 必须包含：
1. 不用手写 specs/ 替代 spec-workflow-mcp。
2. 不用临时 prompt 替代 TDD Skill。
3. 不跳过 Red 阶段直接写实现。
4. 不一次性完成多个 round。
5. 不提前标记未完成 MCP tasks。
6. 不修改 pom.xml，除非用户明确批准。
7. 不新增依赖，除非用户明确批准。
8. 不接数据库 / JPA / Spring AI / 真实 AI API / Security / 用户系统，除非当前 feature 明确要求。
9. 不执行 git add。
10. 不执行 git commit。

允许修改：
1. skills/spec-tdd-cycle/SKILL.md
2. .agents/skills/spec-tdd-cycle/SKILL.md
3. .claude/skills/spec-tdd-cycle/SKILL.md
4. AGENTS.md / CLAUDE.md，只能添加何时使用 spec-tdd-cycle skill 的简短规则

禁止修改：
1. src/main/java
2. src/test/java
3. pom.xml
4. README.md

完成后输出：
1. 创建/修改了哪些文件。
2. spec-tdd-cycle skill 的结构摘要。
3. 是否同步到 .agents/skills。
4. 是否同步到 .claude/skills。
5. 是否修改 AGENTS.md / CLAUDE.md。
6. 是否修改 Java 代码。
7. 是否修改测试代码。
8. 是否修改 pom.xml。
9. git status 摘要。
10. git diff --stat 摘要。
```
