# 本课推荐 Prompt

```text
目标：
围绕“文档保存功能”练习 AI 输出格式控制。

背景：
当前项目是 ai-doc-summary，已经完成：
1. 第 1 课：最小 Java 21 + Spring Boot 3.x + Maven 项目。
2. 第 2 课：AGENTS.md / CLAUDE.md 项目规则文件。
3. 第 3 课：.gitignore 和 Git baseline commit。
4. 第 3A 课：WORKFLOW.md 初版。
5. 第 4 课：已将“文档保存功能”改写为清晰任务和实现计划。

第 4 课已经确定：
1. 第一版只做文档保存。
2. 接口为 POST /api/documents。
3. 请求 JSON 包含 title 和 content。
4. title 和 content 不能为空，也不能是纯空格。
5. 成功状态码建议为 201 Created。
6. 成功响应第一版只返回 documentId。
7. 参数错误返回 400 Bad Request。
8. 当前只使用内存存储。
9. 不接数据库、不接真实 AI API、不加 Spring AI、不加 Spring Security、不加用户系统、不实现文件上传。

输入：
请参考当前项目结构、AGENTS.md、CLAUDE.md、WORKFLOW.md，以及第 4 课确定的文档保存功能约束。

输出：
请不要修改任何项目文件。
请只在对话中输出以下 5 个 Markdown 章节：

## 1. 产品解释
用非技术语言解释文档保存功能，面向产品经理或业务方。
不要出现 Java 类名、Map、AtomicLong、MockMvc 等实现细节。

## 2. 开发计划
用开发者视角输出实现计划，包括：
- 接口路径
- 请求字段
- 响应字段
- 状态码
- 建议新增类
- 内存存储方案
- 参数校验方式
- 实现步骤

## 3. 接口 JSON 示例
输出：
- 请求 JSON
- 成功响应 JSON
- title 错误响应 JSON
- content 错误响应 JSON

要求：
- JSON 必须放在代码块中。
- 成功响应第一版只返回 documentId。
- 不要在成功响应中返回 title 或 content。

## 4. 测试用例清单
使用 Markdown checkbox 格式。
至少包含：
- 保存成功
- title 为空字符串
- title 为纯空格
- content 为空字符串
- content 为纯空格
- 健康检查接口不受影响

## 5. Code Review Checklist
使用 Markdown checkbox 格式。
重点检查：
- 是否没有修改无关文件
- 是否没有新增依赖
- 是否没有引入数据库 / JPA
- 是否没有引入真实 AI API / Spring AI
- 是否没有引入 Spring Security / 用户系统
- 是否只实现 POST /api/documents
- 是否成功响应只返回 documentId
- 是否有参数校验
- 是否有测试覆盖
- 是否没有遗留占用 8080 的进程

限制：
1. 不要修改任何项目文件。
2. 不要创建新文件。
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
1. 输出严格包含 5 个 Markdown 章节。
2. 产品解释面向非技术人员。
3. 开发计划面向开发者。
4. JSON 示例全部放在代码块中。
5. 成功响应 JSON 只包含 documentId。
6. 测试用例清单使用 Markdown checkbox。
7. Code Review Checklist 使用 Markdown checkbox。
8. 没有输出 Java 实现代码。
9. 没有修改任何项目文件。
```
