# 本课推荐 Prompt

```text
目标：
将“帮我做一个文档保存功能”改写成清晰、可审查的 AI 开发任务，并让 AI 先输出实现计划。

背景：
当前项目是 ai-doc-summary，已经完成：
1. 第 1 课：最小 Java 21 + Spring Boot 3.x + Maven 项目。
2. 第 2 课：AGENTS.md / CLAUDE.md 项目规则文件。
3. 第 3 课：.gitignore 和 Git baseline commit。
4. 第 3A 课：WORKFLOW.md 初版。

当前课程进入第 4 课：从模糊需求到清晰任务。
本课目标不是实现代码，而是把业务需求表达清楚，并让 AI 输出可审查计划。

输入：
请查看当前项目结构、pom.xml、README.md、AGENTS.md、CLAUDE.md、WORKFLOW.md、src/ 和当前 git status。

输出：
请不要修改任何项目文件。
请只输出一份“文档保存功能”的清晰任务说明和实现计划。

请严格按以下结构输出：

## 1. 清晰任务说明

使用 6 段式任务结构：

目标：
背景：
输入：
输出：
限制：
验收标准：

## 2. 需求理解

说明文档保存功能要做什么，以及明确不做什么。

## 3. 建议接口设计

说明：
- HTTP 方法
- 路径
- 请求 JSON
- 成功响应 JSON
- 错误响应 JSON
- 状态码

## 4. 建议新增或修改的类

列出预计需要新增或修改的类，并说明用途。
本课只输出计划，不创建这些类。

## 5. 存储策略

说明当前阶段使用内存存储。
不要引入数据库、JPA、H2、PostgreSQL、MySQL 或 Redis。

## 6. 参数校验策略

说明 title 和 content 的校验规则。
不要新增 Bean Validation 依赖，先使用手写校验。

## 7. 测试计划

至少覆盖：
- 保存成功
- title 为空字符串
- title 为纯空格
- content 为空字符串
- content 为纯空格
- 健康检查接口不受影响

## 8. 风险点

说明可能的设计风险和如何避免过度设计。

## 9. 后续实现任务拆分

把后续实现拆成小步骤，便于第 6～7 课继续使用 Plan-Then-Act 和小步实现。

限制：
1. 不要修改任何项目文件。
2. 不要创建新文件。
3. 不要运行命令。
4. 不要输出 Java 实现代码。
5. 不要修改 pom.xml。
6. 不要新增依赖。
7. 不要接入数据库。
8. 不要接入真实 AI API。
9. 不要加入 Spring AI。
10. 不要加入 Spring Security。
11. 不要加入用户系统。
12. 不要实现文档查询接口。
13. 不要实现摘要生成接口。
14. 不要实现文件上传。
15. 不要运行 mvn spring-boot:run。
16. 不要让任何 Java 进程占用 8080。

功能约束：
1. 第一版只实现文档保存。
2. 接口建议为 POST /api/documents。
3. 请求 JSON 包含 title 和 content。
4. title 和 content 不能为空，也不能是纯空格。
5. 成功状态码建议为 201 Created。
6. 成功响应第一版只返回 documentId。
7. 参数错误返回 400 Bad Request。
8. 当前只使用内存存储。
9. 应用重启后数据丢失是当前阶段可接受限制。

验收标准：
1. 输出包含完整 6 段式任务说明。
2. 计划中明确 POST /api/documents。
3. 请求 JSON 明确包含 title 和 content。
4. 成功响应只包含 documentId。
5. 明确 title/content 不能为空或纯空格。
6. 明确当前只使用内存存储。
7. 明确不接数据库、不接真实 AI API、不加 Spring AI、不加 Spring Security、不加用户系统。
8. 包含测试计划。
9. 包含后续小步实现任务拆分。
10. 确认没有修改任何项目文件。
```
