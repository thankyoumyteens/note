# 本课推荐 Prompt

```text
目标：
进入 TDD Refactor phase。

请对当前 `POST /api/documents/{id}/summary` 的实现进行 Refactor 评估。
请先评估是否需要重构，不要一上来直接改代码。

背景：
当前项目是 `ai-doc-summary`，已经完成：

1. `GET /api/health`
2. `POST /api/documents`
3. `GET /api/documents/{id}`
4. `GET /api/documents/{id}/metadata`
5. `POST /api/documents/{id}/summary`
6. 已完成 TDD Red：先为 summary 行为编写失败测试。
7. 已完成 TDD Green：最小实现让 summary 测试通过。

当前阶段：
TDD Refactor phase：在测试保护下评估并小步重构。

请先读取：

1. `AGENTS.md`
2. `CLAUDE.md`
3. `WORKFLOW.md`
4. 当前 `src/main/java`
5. 当前 `src/test/java`
6. 当前 `git status`
7. 当前 `git diff`

第一步：
请先不要改代码。
先输出 Refactor 评估报告：

1. 当前 summary 实现涉及哪些类和测试。
2. 当前实现是否已经足够简单。
3. 是否存在 Controller 过重。
4. 是否存在重复代码。
5. 是否存在命名不清。
6. 是否存在不必要抽象。
7. 是否存在过度设计。
8. 是否存在项目边界风险。
9. 是否需要重构。
10. 如果需要，只列出最小重构计划。

重构边界：

1. 只允许重构已有 summary 相关实现。
2. 不新增业务功能。
3. 不修改 API 行为。
4. 不修改响应 JSON 结构。
5. 不降低测试断言。
6. 不删除已有 summary 测试。
7. 不删除 404 测试。
8. 不修改 `pom.xml`。
9. 不新增依赖。
10. 不接真实 AI API。
11. 不接 Spring AI。
12. 不接数据库 / JPA。
13. 不加 Spring Security / 用户系统。
14. 不实现缓存 / 历史 / 异步任务。
15. 不运行 `mvn spring-boot:run`。
16. 不执行 `git add`。
17. 不执行 `git commit`。

如果评估认为不需要重构：
请明确说明原因，然后运行 `mvn test`，输出测试结果、`git status` 和结论。

如果评估认为需要重构：
请按小步执行：

1. 每次只做一个重构动作。
2. 每步说明改了哪些文件。
3. 每步后运行相关测试，必要时运行 `mvn test`。
4. 每步后输出 `git diff --stat`。
5. 如果测试失败，先解释原因，不要继续扩大修改。

完成后输出：

1. 是否进行了重构。
2. 如果没有重构，为什么不需要。
3. 如果进行了重构，修改了哪些文件。
4. 是否修改了 API 行为。
5. 是否修改了测试断言。
6. 是否修改了 `pom.xml`。
7. 是否新增依赖。
8. 是否引入真实 AI API / Spring AI / 数据库 / JPA / Security / 用户系统。
9. `mvn test` 结果。
10. `git status` 摘要。
11. `git diff --stat` 摘要。
12. 是否建议进入 TDD workflow tooling。
```
