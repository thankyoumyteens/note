# 本课推荐 Prompt

```text
目标：
为当前 ai-doc-summary 项目创建 AI agent 项目规则文件，包括 AGENTS.md 和 CLAUDE.md。

背景：
当前项目是 AI 工具驱动开发工作流课程的实战项目。
项目已经完成第 1 课：从空目录创建最小可运行 Java 21 + Spring Boot 3.x + Maven 项目。
当前项目已通过：
1. mvn test
2. mvn spring-boot:run
3. GET /api/health

输入：
请查看当前项目结构、pom.xml、README.md 和 src/。

输出：
请创建：
1. AGENTS.md：偏工具中立，兼容 Codex / Codex CLI。
2. CLAUDE.md：兼容 Claude Code，可加入 Claude Code 专属工作流规则。

AGENTS.md 至少包含：
1. Project Role
2. Stack
3. Commands
4. Code Rules
5. Workflow
6. Runtime / Port Rules
7. Security Rules
8. Review Checklist

CLAUDE.md 至少包含：
1. Project Role
2. Development Stack
3. Claude Code Rules
4. Coding Rules
5. Runtime / Port Rules
6. Security Rules
7. Review Checklist
8. Future Tooling Notes

限制：
1. 不要修改 pom.xml。
2. 不要修改 Java 源码。
3. 不要修改测试代码。
4. 不要新增依赖。
5. 不要加入数据库。
6. 不要加入 Spring Security。
7. 不要加入 Docker。
8. 不要加入前端。
9. 不要接入真实 AI API。
10. 不要加入 Spring AI。
11. 不要创建复杂目录。
12. 不要运行 mvn spring-boot:run。
13. 如果需要验证，只能运行 mvn test。
14. 不要让任何 Java 进程长期占用 8080。

规则要求：
1. 对非平凡修改，必须先计划，再执行。
2. 修改代码后，应运行相关测试。
3. 行为变更必须新增或更新测试。
4. 不要修改无关文件。
5. 不要新增依赖，除非得到明确确认。
6. 不要硬编码 secret、token、API key 或敏感信息。
7. 运行 mvn spring-boot:run 验证启动后，必须停止 Spring Boot 进程。
8. 如果 8080 被占用，需要提示用户用 lsof -i tcp:8080 检查，并停止对应 Java 进程。
9. 后续课程会逐步引入 MCP、Skills、Commands、Hooks、Spec Workflow 工具化，但当前不要实现这些工具，只在 Future Tooling Notes 中记录。

验收标准：
1. 根目录存在 AGENTS.md。
2. 根目录存在 CLAUDE.md。
3. 两个文件规则大体一致。
4. 两个文件都包含 mvn test 和 mvn spring-boot:run。
5. 两个文件都明确不要加入数据库、Security、Docker、前端、真实 AI API、Spring AI。
6. 两个文件都明确非平凡修改先计划再执行。
7. 两个文件都明确行为变更要配测试。
8. 两个文件都明确禁止硬编码密钥。
9. 两个文件都包含 8080 端口占用处理规则。
10. 不修改 pom.xml、Java 源码或测试代码。
11. 完成后请总结创建了哪些文件，以及后续如何使用它们。
```

平凡修改: 不需要先单独写计划，可以直接改，但改完仍然要总结变更，必要时运行测试。

这些一般算平凡修改：

1. 改 README 里的错别字
2. 改注释
3. 改日志文案
4. 改测试名称
5. 改一个明显的拼写错误
6. 删除无用 import
7. 格式化单个文件
8. 修改一个很小的文档片段
9. 改一个常量名，但不改变值和行为
10. 修复一个非常明确的 typo，例如 docuemnt → document
