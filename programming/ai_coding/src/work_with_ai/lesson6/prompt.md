# 本课推荐 Prompt

```text
目标：
为“文档保存功能”制定可审查的实现计划。请先不要改代码。

背景：
当前项目是 ai-doc-summary，已经完成：
1. 第 1 课：最小 Java 21 + Spring Boot 3.x + Maven 项目。
2. 第 2 课：AGENTS.md / CLAUDE.md 项目规则文件。
3. 第 3 课：.gitignore 和 Git baseline commit。
4. 第 3A 课：WORKFLOW.md 初版。
5. 第 4 课：将“文档保存功能”改写为清晰任务。
6. 第 5 课：围绕文档保存功能练习输出格式控制。
7. 第 5A 课：在 WORKFLOW.md 中设计 Prompt Tooling: Commands and Skills。

现在进入第 6 课：先计划，后执行。
本课只做 Plan，不进入 Act。

第 4～5 课已经确定的文档保存功能约束：
1. 第一版只做文档保存。
2. 接口为 POST /api/documents。
3. 请求 JSON 包含 title 和 content。
4. title 和 content 不能为空，也不能是纯空格。
5. 成功状态码建议为 201 Created。
6. 成功响应第一版只返回 documentId。
7. 参数错误返回 400 Bad Request。
8. 当前只使用内存存储。
9. 不接数据库。
10. 不使用 JPA。
11. 不新增依赖。
12. 不接真实 AI API。
13. 不加入 Spring AI。
14. 不加入 Spring Security。
15. 不加入用户系统。
16. 不实现文件上传。
17. 不实现文档查询接口。
18. 不实现摘要生成接口。

输入：
请查看当前项目结构、pom.xml、README.md、AGENTS.md、CLAUDE.md、WORKFLOW.md、src/ 和当前 git status。

输出：
请不要修改任何项目文件。
请不要创建任何新文件。
请不要运行任何命令。
请只输出“文档保存功能”的实现计划。

请严格按以下 Markdown 章节输出：

## 1. 需求理解
说明本次要实现什么，以及明确不做什么。

## 2. 涉及文件
列出预计后续第 7 课需要新增或修改的文件。
每个文件说明用途。
同时说明哪些文件不应该修改，例如 pom.xml、README.md、AGENTS.md、CLAUDE.md、WORKFLOW.md。

## 3. 修改步骤
按小步骤列出后续实现顺序。
步骤要足够小，便于第 7 课逐步执行。

## 4. 数据结构 / API 变化
说明：
- 请求 JSON
- 成功响应 JSON
- 参数错误响应 JSON
- HTTP 状态码
- 内存数据结构
- documentId 生成方式

要求：
成功响应只允许包含 documentId，不允许包含 title 或 content。

## 5. 测试计划
列出后续需要新增或更新的测试。
至少包含：
- 保存成功
- title 为空字符串
- title 为纯空格
- content 为空字符串
- content 为纯空格
- 健康检查接口不受影响

## 6. 风险和回滚方式
说明：
- 可能的设计风险
- 如何避免过度设计
- 如何检查 git diff
- 如果实现失败如何回滚

## 7. 计划自检
使用 Markdown checkbox 格式检查：
- 是否没有数据库
- 是否没有 JPA
- 是否没有新增依赖
- 是否没有真实 AI API
- 是否没有 Spring AI
- 是否没有 Spring Security
- 是否没有用户系统
- 是否没有文件上传
- 是否没有查询接口
- 是否没有摘要接口
- 是否成功响应只返回 documentId
- 是否包含测试计划
- 是否本课没有修改文件

限制：
1. 不要修改任何项目文件。
2. 不要创建任何新文件。
3. 不要运行命令。
4. 不要输出 Java 实现代码。
5. 不要修改 pom.xml。
6. 不要新增依赖。
7. 不要接入数据库、JPA、H2、PostgreSQL、MySQL 或 Redis。
8. 不要接入真实 AI API。
9. 不要加入 Spring AI。
10. 不要加入 Spring Security。
11. 不要加入用户系统。
12. 不要实现文档查询接口。
13. 不要实现摘要生成接口。
14. 不要实现文件上传。
15. 不要运行 mvn spring-boot:run。
16. 不要让任何 Java 进程占用 8080。

验收标准：
1. 输出严格包含 7 个 Markdown 章节。
2. 涉及文件列表清晰。
3. 修改步骤可以直接转化为第 7 课的小步实现任务。
4. API 设计中成功响应只包含 documentId。
5. 测试计划覆盖成功路径和参数错误路径。
6. 风险和回滚方式明确。
7. 计划自检全部符合限制。
8. 明确确认本课没有修改任何项目文件。
```
