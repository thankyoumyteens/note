# 本课推荐 Prompt

```text
目标：
进入 TDD Green phase。

请基于当前已经写好的 summary 失败测试，实现 `POST /api/documents/{id}/summary`。
当前目标是：只写最小实现，让现有失败测试通过。

背景：
当前项目是 `ai-doc-summary`，已经完成：

1. `POST /api/documents` 文档保存功能。
2. `GET /api/documents/{id}` 文档查询功能。
3. `GET /api/documents/{id}/metadata` 文档元信息查询功能。
4. 已经为 `POST /api/documents/{id}/summary` 写好失败测试。
5. 当前阶段允许写最小实现，但不做额外重构和功能扩展。

请先读取：

1. `AGENTS.md`
2. `CLAUDE.md`
3. `WORKFLOW.md`
4. 当前 `src/main/java`
5. 当前 `src/test/java`
6. 当前 `git status`
7. 当前 summary 相关失败测试

第一步：
请先不要改代码。
先输出：

1. 当前失败测试覆盖了哪些行为。
2. 失败原因是否是 summary 接口尚未实现或行为尚未满足。
3. 为了让测试通过，最小需要修改哪些文件。
4. 是否需要新增 `SummaryController` / `SummaryService` / `FakeAiSummaryClient` / `SummaryResponse`。
5. 是否需要修改 `InMemoryDocumentStore`。
6. 是否存在过度设计风险。

等我确认后，再进入实现。

实现要求：

1. 实现 `POST /api/documents/{id}/summary`。
2. 文档存在时返回 `200 OK`。
3. 响应包含 `documentId` 和 `summary`。
4. `summary` 必须符合当前测试中的固定 fake 规则，例如 `"Summary: " + content`。
5. 文档不存在时返回 `404 Not Found`。
6. 使用 `FakeAiSummaryClient` 或本地 fake service。
7. 只使用内存存储。
8. 保持实现最小。
9. 不顺手重构无关代码。
10. 不改变已有 `POST /api/documents`、`GET /api/documents/{id}`、`GET /api/documents/{id}/metadata` 接口行为。

禁止事项：

1. 不要修改 `pom.xml`。
2. 不要新增 Java 依赖。
3. 不要接真实 AI API。
4. 不要接 Spring AI。
5. 不要加入数据库 / JPA。
6. 不要加入 Spring Security / 用户系统。
7. 不要实现摘要缓存。
8. 不要实现摘要历史。
9. 不要实现异步摘要任务。
10. 不要实现文件上传。
11. 不要运行 `mvn spring-boot:run`。
12. 不要执行 `git add`。
13. 不要执行 `git commit`。

测试要求：

1. 运行 `mvn test`。
2. summary 相关测试应通过。
3. 已有 `POST /api/documents` 测试应通过。
4. 已有 `GET /api/documents/{id}` 测试应通过。
5. 已有 `GET /api/documents/{id}/metadata` 测试应通过。
6. `GET /api/health` 测试应通过。

完成后输出：

1. 新增/修改了哪些文件。
2. 实现了哪些最小代码。
3. `mvn test` 结果。
4. `git status` 摘要。
5. `git diff --stat` 摘要。
6. 是否修改 `pom.xml`。
7. 是否新增依赖。
8. 是否接入真实 AI API / Spring AI。
9. 是否引入数据库 / JPA / Security / 用户系统。
10. 是否有任何越界修改。
11. 是否还有需要进入 Refactor phase 的问题，但当前阶段不要执行重构。
```
