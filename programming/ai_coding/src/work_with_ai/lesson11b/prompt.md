# 本课推荐 Prompt

```text
目标：
为当前项目创建 TDD Skill 工作流。

任务目标：
把 TDD 的 Red / Green / Refactor 三个阶段固化成可复用 Skill。
不要继续写业务功能，不要修改 Java 代码，不要修改测试代码。

背景：
当前项目是 ai-doc-summary，已经完成：
1. GET /api/health
2. POST /api/documents
3. GET /api/documents/{id}
4. GET /api/documents/{id}/metadata
5. POST /api/documents/{id}/summary
6. 已完成 TDD Red 实践：先写失败测试。
7. 已完成 TDD Green 实践：最小实现让测试通过。
8. 已完成 TDD Refactor 实践：在测试保护下小步重构。

当前工作流设计：
1. 高频 TDD 流程优先沉淀为 Skill。
2. WORKFLOW.md 只保留工作流索引和选择规则。
3. 后续中等复杂度 feature 将使用 spec-workflow-mcp + TDD Skill 组合实践。

请先读取：
1. AGENTS.md
2. CLAUDE.md
3. WORKFLOW.md
4. 当前 git status

第一步：
请先不要改文件。
先输出 TDD Skill 设计计划，说明：
1. 准备创建哪些 Skill
2. 每个 Skill 的用途
3. 每个 Skill 的输入
4. 每个 Skill 的输出
5. 每个 Skill 的禁止事项
6. 每个 Skill 的完成标准
7. 是否需要小幅更新 WORKFLOW.md
8. 是否需要小幅更新 AGENTS.md / CLAUDE.md

确认计划后，再创建或修改文件。

允许新增：
1. skills/tdd-red/SKILL.md
2. skills/tdd-green/SKILL.md
3. skills/tdd-refactor/SKILL.md

可选新增：
1. skills/tdd-cycle/SKILL.md

允许小幅修改：
1. WORKFLOW.md
2. AGENTS.md
3. CLAUDE.md

修改要求：
1. WORKFLOW.md 只写 TDD Skill 索引和选择规则，不写长篇执行细节。
2. AGENTS.md / CLAUDE.md 只写何时必须使用 TDD Skill 的默认规则。
3. Skill 内容必须兼容 Codex 和 Claude Code，不写成只适合某一个工具。

禁止修改：
1. 不修改 src/main/java
2. 不修改 src/test/java
3. 不修改 pom.xml
4. 不新增依赖
5. 不实现新接口
6. 不修改已有接口行为
7. 不接真实 AI API
8. 不接 Spring AI
9. 不接数据库 / JPA
10. 不加入 Spring Security / 用户系统
11. 不运行 mvn spring-boot:run
12. 不执行 git add
13. 不执行 git commit

每个 Skill 必须包含：
1. Purpose
2. When to use
3. Inputs
4. Steps
5. Output format
6. Hard rules
7. Completion checklist
8. Common mistakes to avoid

tdd-red 必须强调：
1. 只写测试，不写实现
2. 只允许修改测试文件
3. 测试应该失败
4. 失败原因必须是功能尚未实现或行为尚未满足
5. 不允许提前实现业务代码

tdd-green 必须强调：
1. 先读取失败测试
2. 只写最小实现
3. 不降低测试断言
4. 不删除测试
5. 不扩大功能范围
6. mvn test 必须通过

tdd-refactor 必须强调：
1. 测试通过后才允许进入 Refactor
2. 先评估是否需要重构
3. 不为了改而改
4. 不新增业务功能
5. 不修改 API 行为
6. 不降低测试断言
7. 每步重构后运行测试

完成后输出：
1. 创建/修改了哪些文件
2. 每个 Skill 的主要内容摘要
3. WORKFLOW.md 是否只保留索引和选择规则
4. 是否修改 AGENTS.md / CLAUDE.md
5. 是否修改 src/main/java
6. 是否修改 src/test/java
7. 是否修改 pom.xml
8. 是否新增依赖
9. 是否运行 mvn test
10. git status 摘要
11. git diff --stat 摘要
12. 是否可以进入 spec-workflow-mcp + TDD Skill 组合实践
```
