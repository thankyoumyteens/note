# 本课推荐 Prompt

```text
目标：
更新 WORKFLOW.md，新增 Plan-Then-Act Tooling 章节，把第 6～7 课形成的经验沉淀为可复用工作流。

背景：
当前项目是 ai-doc-summary，已经完成：
1. 第 1 课：最小 Java 21 + Spring Boot 3.x + Maven 项目。
2. 第 2 课：AGENTS.md / CLAUDE.md 项目规则文件。
3. 第 3 课：.gitignore 和 Git baseline commit。
4. 第 3A 课：WORKFLOW.md 初版。
5. 第 4 课：将“文档保存功能”改写为清晰任务。
6. 第 5 课：围绕文档保存功能练习输出格式控制。
7. 第 5A 课：在 WORKFLOW.md 中设计 Prompt Tooling: Commands and Skills。
8. 第 6 课：先计划，后执行。
9. 第 7 课：小步实现文档保存功能。

第 7 课发现：
Codex 和 Claude Code 都可能自带 Plan-Then-Act 行为。
但 AI 自带 plan 不等于真正小步执行。
AI 可能一次性执行多个 plan item，例如一次性生成 DTO、Model、Store、Controller 和 Test。
因此需要把 Plan-Then-Act 工具化为：
1. AI 先生成 plan。
2. 人类确认 plan。
3. AI 每次只执行下一个未完成 plan item。
4. 每个 plan item 完成后立即停止。
5. 输出修改文件、diff 摘要、测试建议和下一步建议。
6. 等待人类确认后再继续。

输入：
请查看当前项目结构、WORKFLOW.md、AGENTS.md、CLAUDE.md 和当前 git status。

输出：
请只更新 WORKFLOW.md，新增一个章节：

## Plan-Then-Act Tooling

该章节需要包含：

1. Why Plan-Then-Act Still Needs Tooling
   - Codex / Claude Code 可能自带 plan 能力
   - 但自带 plan 不等于真正小步执行
   - 人类仍需控制执行粒度、diff 和验收

2. Correct Plan-Then-Act Loop
   - Generate plan
   - Human reviews plan
   - Implement next unfinished plan item only
   - Stop after one item
   - Report diff / tests / risks
   - Wait for human confirmation
   - Continue or rollback

3. Bad Pattern
   - 一次性执行所有 plan item
   - 一次性生成多个相关文件
   - 没有等待确认
   - 没有分步 diff
   - 把 plan 当 todo list 全部自动完成

4. Good Pattern
   - 每次只执行下一个未完成 plan item
   - 完成后停止
   - 输出本次修改文件
   - 输出 git diff --stat 摘要
   - 输出是否越界
   - 输出下一步建议，但不执行

5. /plan Command Design
   - 用途
   - 输入
   - 输出
   - 限制
   - 验收标准
   - 示例调用
   - 示例输出结构

6. /implement-next-step Command Design
   - 用途
   - 输入
   - 输出
   - 限制
   - 验收标准
   - 示例调用
   - 示例输出结构
   - 必须强调：只执行下一个未完成 plan item，完成后停止

7. /review-diff Command Design
   - 用途
   - 输入
   - 输出
   - 限制
   - 验收标准
   - 示例调用
   - 示例输出结构

8. Git Safety Rules
   - 修改前检查 git status
   - 每步后检查 git diff --stat
   - 不执行 git add
   - 不执行 git commit
   - 发现越界修改时先停下来
   - 需要时用 git restore 回退单文件
   - 极端情况下才用 git reset --hard HEAD

9. Future Implementation Notes
   - 后续可迁移到 Claude Slash Commands
   - 后续可迁移到 Claude Skills
   - 后续可迁移到 Codex Skills
   - 当前阶段只记录设计，不创建正式 .claude/commands 或 skills 目录

限制：
1. 不要修改 pom.xml。
2. 不要修改 Java 源码。
3. 不要修改测试代码。
4. 不要修改 README.md。
5. 不要修改 AGENTS.md。
6. 不要修改 CLAUDE.md。
7. 不要修改 COURSE.md。
8. 不要新增依赖。
9. 不要创建 .claude/commands/ 目录。
10. 不要创建 skills/ 目录。
11. 不要创建 hooks/ 目录。
12. 不要运行 mvn spring-boot:run。
13. 如果需要验证，只能运行 mvn test。
14. 不要执行 git add。
15. 不要执行 git commit。
16. 不要继续实现新业务功能。

验收标准：
1. WORKFLOW.md 中新增 Plan-Then-Act Tooling 章节。
2. 章节中明确说明 AI 自带 plan 不等于真正小步执行。
3. 章节中明确 Correct Plan-Then-Act Loop。
4. 章节中包含 Bad Pattern 和 Good Pattern。
5. 章节中包含 /plan 设计。
6. 章节中包含 /implement-next-step 设计。
7. 章节中包含 /review-diff 设计。
8. 章节中包含 Git Safety Rules。
9. 章节中明确当前不创建正式工具目录。
10. 没有修改业务代码。
11. 没有新增依赖。
12. 完成后总结修改了哪些文件。
```
