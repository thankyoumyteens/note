# 本课推荐 Prompt

你现在在 `ai-doc-summary` 项目根目录里，把下面这段发给 **Codex** 或 **Claude Code**：

```text
目标：
为当前 ai-doc-summary 项目创建 AI agent 项目规则文件，包括 AGENTS.md 和 CLAUDE.md。

背景：
当前项目是第 1 课创建的最小 Java 21 + Spring Boot 3.x + Maven 项目。项目后续会逐步实现文档保存、文档查询、AI 摘要生成、真实 AI Provider 接入、测试、审查和重构。当前项目还没有数据库、Spring Security、Docker、前端或真实 AI API。

输入：
请查看当前项目结构、pom.xml、README.md 和已有测试。

输出：
请创建：
1. AGENTS.md：偏工具中立，优先兼容 Codex / Codex CLI。
2. CLAUDE.md：兼容 Claude Code，可包含 Claude Code 专属工作流建议。
3. lessons/lesson-02-project-rules.md：记录本课学习笔记、生成的规则文件用途、后续如何使用。

AGENTS.md 至少包含：
1. Project Role
2. Stack
3. Commands
4. Code Rules
5. Workflow
6. Security Rules
7. Review Checklist

CLAUDE.md 至少包含：
1. Project Role
2. Development Stack
3. Claude Code Rules
4. Coding Rules
5. Security Rules
6. Review Checklist

限制：
1. 不要修改 pom.xml。
2. 不要修改 Java 源码。
3. 不要新增依赖。
4. 不要加入数据库、Spring Security、Docker、前端或真实 AI API。
5. 不要把规则写得太长，保持清晰、可执行。
6. 不要写任何真实 API key 或密钥。
7. 不要修改 README.md，除非你先说明理由并等待确认。

验收标准：
1. 项目根目录存在 AGENTS.md。
2. 项目根目录存在 CLAUDE.md。
3. 存在 lessons/lesson-02-project-rules.md。
4. AGENTS.md 和 CLAUDE.md 的规则大体一致。
5. 两个规则文件都包含测试命令 mvn test 和启动命令 mvn spring-boot:run。
6. 明确要求后续非平凡修改先计划再执行。
7. 明确要求行为变更需要新增或更新测试。
8. 明确禁止硬编码 API key、密钥或敏感信息。
9. 不修改业务代码。
10. 完成后请总结创建了哪些文件，以及后续如何使用它们。
```
