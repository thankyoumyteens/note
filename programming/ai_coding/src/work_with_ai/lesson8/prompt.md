# 推荐发给 Codex 的 Prompt

```text
目标：
为文档查询功能 GET /api/documents/{id} 编写轻量 Spec。当前只写规格文件，不实现代码。

背景：
当前项目是 ai-doc-summary，已经完成：
1. 最小 Spring Boot 项目
2. AGENTS.md / CLAUDE.md
3. Git baseline
4. WORKFLOW.md
5. POST /api/documents 文档保存功能
6. Plan-Then-Act Tooling 工作流沉淀

现在进入第 8 课：轻量 Spec 结构。

本课目标：
创建 specs/document-query/ 目录，并编写：
1. requirements.md
2. design.md
3. tasks.md
4. test.md

功能说明：
新增文档查询接口：

GET /api/documents/{id}

功能范围：
1. 根据 documentId 查询内存中已保存的文档。
2. 查询成功返回 documentId、title、content。
3. documentId 不存在时返回 404 Not Found。
4. 当前仍然只使用内存存储。
5. 不接数据库。
6. 不使用 JPA。
7. 不新增依赖。
8. 不接真实 AI API。
9. 不加入 Spring AI。
10. 不加入 Spring Security。
11. 不加入用户系统。
12. 不实现分页。
13. 不实现搜索。
14. 不实现文件上传。
15. 不实现摘要生成。

输入：
请查看当前项目结构、AGENTS.md、CLAUDE.md、WORKFLOW.md、src/ 和当前 git status。

输出：
请只创建以下规格文件：

specs/document-query/requirements.md
specs/document-query/design.md
specs/document-query/tasks.md
specs/document-query/test.md

不要修改 Java 源码。
不要修改测试代码。
不要修改 pom.xml。
不要修改 README.md。
不要修改 AGENTS.md。
不要修改 CLAUDE.md。
不要修改 WORKFLOW.md。
不要修改 COURSE.md。
不要新增依赖。
不要运行 mvn spring-boot:run。
不要执行 git add。
不要执行 git commit。

requirements.md 需要包含：
1. Feature Summary
2. User Story
3. Scope
4. Non-goals
5. Functional Requirements
6. Acceptance Criteria

design.md 需要包含：
1. API Design
2. Request
3. Success Response
4. Error Response
5. HTTP Status Codes
6. Data Source
7. Expected Code Changes
8. Design Constraints

tasks.md 需要包含：
1. Task checklist
2. 每个任务使用 Markdown checkbox
3. 每个任务必须足够小，适合后续按 /implement-next-step 执行
4. 不要把所有实现合并成一个大任务

test.md 需要包含：
1. Test Scope
2. Success cases
3. Error cases
4. Regression cases
5. Out-of-scope tests

验收标准：
1. 创建 specs/document-query/ 目录。
2. 创建 requirements.md、design.md、tasks.md、test.md。
3. 明确 GET /api/documents/{id}。
4. 成功响应包含 documentId、title、content。
5. 不存在时返回 404。
6. 明确只使用内存存储。
7. 明确不接数据库、不用 JPA、不加依赖、不接 Spring AI、不接真实 AI API。
8. tasks.md 使用 checkbox。
9. 本课不实现 Java 代码。
10. 完成后输出创建了哪些文件和 git status 摘要。
```
