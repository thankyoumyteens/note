# 指挥 AI 工作

| 阶段                                | 课号 | 课程                                    | 类型          | 目标                                                             | 主要工具 / 产物                                                 |
| ----------------------------------- | ---: | --------------------------------------- | ------------- | ---------------------------------------------------------------- | --------------------------------------------------------------- |
| 第 1 阶段：从零启动项目             |    1 | 把“我要一个 Java 项目”变成清晰任务      | 方法课        | 从空目录指挥 AI 创建最小可运行 Spring Boot 项目                  | Spring Boot 最小项目                                            |
|                                     |    2 | 建立项目规则文件 AGENTS.md / CLAUDE.md  | 方法 + 工具课 | 建立 Codex / Claude Code 都能读取的项目级规则                    | `AGENTS.md`、`CLAUDE.md`                                        |
|                                     |    3 | 初始化 Git 与基线提交                   | 方法课        | 建立可审查、可回滚的 baseline                                    | `.gitignore`、baseline commit                                   |
|                                     |   3A | 项目启动流程工具化                      | 工具课        | 把项目初始化、规则文件、baseline checklist 固化                  | Spring Initializr、Maven Wrapper、Git baseline checklist        |
| 第 2 阶段：基础指令能力             |    4 | 从模糊需求到清晰任务                    | 方法课        | 学会把模糊需求改写成 AI 可执行任务                               | 目标 / 背景 / 输入 / 输出 / 限制 / 验收标准                     |
|                                     |    5 | 输出格式控制                            | 方法课        | 控制 AI 输出产品解释、开发计划、JSON、测试清单、review checklist | Markdown、JSON、checkbox checklist                              |
|                                     |   5A | Prompt 模板工具化：Commands / Skills    | 工具课        | 把常用 prompt 固化成可复用命令或技能                             | Codex Skills、Claude Skills、Claude slash commands              |
| 第 3 阶段：Plan-Then-Act 与小步实现 |    6 | 先计划，后执行                          | 方法课        | 让 AI 先输出可审查计划，不直接改代码                             | Plan checklist                                                  |
|                                     |    7 | 小步实现文档保存功能                    | 方法课        | 按计划小步实现，保持小 diff                                      | `POST /api/documents`                                           |
|                                     |   7A | Plan-Then-Act 工具化                    | 工具课        | 把“计划 → 执行 → diff → 测试 → 总结”固化为命令/skill             | `/plan`、`/implement-step`、Codex skill、Git branch/worktree    |
| 第 4 阶段：Spec Workflow            |    8 | 轻量 Spec 结构                          | 方法课        | 手写 `requirements/design/tasks/test`，理解 spec 本质            | `specs/document-query/`                                         |
|                                     |    9 | Spec 驱动实现文档查询功能               | 方法课        | 让 AI 读取 spec、执行 tasks、更新状态                            | `GET /api/documents/{id}`                                       |
|                                     |   9A | Spec Workflow 工具化：spec-workflow-mcp | 工具课        | 用 MCP 管理 spec、任务、进度和审批                               | `@pimzino/spec-workflow-mcp`、dashboard                         |
|                                     |   9B | 用 spec-workflow-mcp 复做一个小功能     | 工具实践课    | 把手写 spec 流程迁移到 MCP 工具流                                | MCP spec、任务状态、审批记录                                    |
| 第 5 阶段：TDD with AI              |   10 | 先写测试，不写实现                      | 方法课        | 用测试先定义正确行为                                             | 摘要功能测试                                                    |
|                                     |   11 | 最小实现让测试通过                      | 方法课        | 使用 Fake client / 固定逻辑完成摘要功能闭环                      | `FakeAiSummaryClient` 或本地 fake service                       |
|                                     |  11A | 测试工作流工具化                        | 工具课        | 自动化测试运行、分类、覆盖率和失败分析                           | Maven Surefire、Failsafe、JaCoCo、Claude Hooks                  |
| 第 6 阶段：AI 工具工作流集成        |   12 | MCP 基础与项目接入                      | 工具课        | 理解 MCP 如何把外部工具接入 AI coding agent                      | MCP server 配置、工具权限边界                                   |
|                                     |   13 | 项目级 Skills / Commands 设计           | 工具课        | 为本项目沉淀可复用开发命令                                       | `/new-feature`、`/review-diff`、`/write-handoff`                |
|                                     |  13A | Hooks 自动化：测试、格式化、提醒        | 工具课        | 把重复动作自动触发，减少手动操作                                 | Claude Hooks、test hook、format hook                            |
|                                     |  13B | 工具权限与安全边界                      | 工具课        | 控制 AI 工具能做什么、不能做什么                                 | allowlist、危险命令拦截、secret 防护                            |
| 第 7 阶段：AI Code Review           |   14 | 功能审查与回归审查                      | 方法课        | 让 AI 审查 diff、兼容性、测试和过度设计                          | Review prompt                                                   |
|                                     |   15 | Java 后端专项审查                       | 方法课        | 审查 Controller、Service、DTO、异常、日志、配置                  | Java backend checklist                                          |
|                                     |  15A | Code Review 工具化                      | 工具课        | 把 review 固化为 PR checklist / skill / 自动扫描                 | Codex GitHub review、Claude review command、Semgrep/CodeQL 可选 |
| 第 8 阶段：重构、文档与长期维护     |   16 | 安全小步重构                            | 方法课        | 先调查，再小步重构，保持测试通过                                 | Refactor checklist                                              |
|                                     |   17 | 生成项目文档和 Handoff                  | 方法课        | 让新会话可以继续项目                                             | `README.md`、`HANDOFF.md`                                       |
|                                     |   18 | Commands / Skills / Hooks 自动化        | 工具课        | 把重复流程变成可复用动作                                         | Claude Hooks、Claude Skills、Codex Skills                       |
|                                     |  18A | MCP / Skills / Hooks 组合工作流         | 综合工具课    | 把 spec、TDD、review、handoff 串成完整工作流                     | MCP + Skills + Hooks + AGENTS/CLAUDE                            |
|                                     |  18B | 最终项目验收与流程固化                  | 综合课        | 输出可复制到下一个项目的 AI 开发工作流                           | `WORKFLOW.md`、最终 checklist                                   |
