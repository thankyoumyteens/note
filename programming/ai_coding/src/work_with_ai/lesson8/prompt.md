# 推荐发给 Codex 的 Prompt

在项目根目录运行 Codex，发送：

```text
目标：
开始第 8 课：为文档查询功能创建轻量 Spec 结构。请只创建 spec 文件，不要实现代码。

背景：
当前项目是 ai-doc-summary，已经完成：
1. 最小 Spring Boot 项目
2. AGENTS.md / CLAUDE.md
3. Git baseline
4. POST /api/documents 文档保存功能
5. 文档保存功能使用内存存储
6. POST /api/documents 成功响应只返回 documentId
7. mvn test 已通过

现在要为下一个功能创建轻量 spec：
GET /api/documents/{id}

输入：
请查看当前项目结构、AGENTS.md、CLAUDE.md、README.md、src/、tests/ 和当前 git status。
如果需要了解当前文档保存实现，可以只阅读相关 document 包和测试。

输出：
请创建目录和文件：
1. specs/document-query/requirements.md
2. specs/document-query/design.md
3. specs/document-query/tasks.md
4. specs/document-query/test.md
5. lessons/lesson-08-lightweight-spec.md

requirements.md 必须包含：
1. Goal
2. User Story
3. Scope
4. Non-goals
5. Acceptance Criteria

design.md 必须包含：
1. Current System
2. Proposed Changes
3. Affected Files
4. Data/API Changes
5. Risks

tasks.md 必须包含可执行任务列表，使用 Markdown checkbox：
- [ ] Task 1
- [ ] Task 2

test.md 必须包含：
1. Unit Tests
2. Integration Tests
3. Manual Checks
4. Regression Risks

功能约束：
1. 实现目标是 GET /api/documents/{id}
2. 查询成功返回 200 OK
3. 查询成功响应包含 documentId、title、content
4. 查询不存在的文档返回 404 Not Found
5. 错误响应可以保持简单，例如 {"error":"document not found"}
6. 继续使用当前内存存储
7. 不接数据库
8. 不接 AI API
9. 不加入用户系统
10. 不加入 Spring Security
11. 不新增依赖
12. 不实现文档列表查询
13. 不实现摘要功能
14. 不改变 POST /api/documents 的成功响应格式

限制：
1. 不要修改 Java 源码。
2. 不要修改 pom.xml。
3. 不要新增依赖。
4. 不要修改 README.md，除非你先说明理由并等待确认。
5. 不要实现 GET /api/documents/{id}。
6. 本课只创建 spec 和 lesson 笔记。
7. 不要运行测试，除非只是说明后续测试命令。

验收标准：
1. specs/document-query/ 下存在 requirements.md、design.md、tasks.md、test.md。
2. lessons/lesson-08-lightweight-spec.md 存在。
3. spec 明确 Scope 和 Non-goals。
4. spec 明确 GET /api/documents/{id} 的请求、成功响应、错误响应和状态码。
5. tasks.md 可以直接作为第 9 课实现任务输入。
6. test.md 覆盖查询成功、查询不存在、POST 接口不受影响、健康检查不受影响。
7. 没有修改 Java 源码、pom.xml 或 README.md。
8. 完成后请总结创建了哪些文件，以及第 9 课如何使用这些 spec。
```

## 你要检查 Codex 的输出

重点检查 8 点：

```text
1. 是否只创建 specs/document-query/ 和 lesson 笔记
2. 是否没有实现 Java 代码
3. 是否没有修改 pom.xml
4. 是否没有新增依赖
5. 是否明确 Scope
6. 是否明确 Non-goals
7. 是否明确成功和失败响应
8. tasks.md 是否能直接指导第 9 课实现
```
