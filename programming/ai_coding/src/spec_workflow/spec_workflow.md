# Spec Workflow

Spec-workflow（规范工作流）是一种专门为 AI 代码生成和 Autonomous Agents（自主智能体）设计的“规范驱动开发”（Spec-Driven Development, SDD）方法论及生态系统。

它的核心目的是为 AI 编程建立规矩。随着 AI 应用的复杂化，如果直接让 AI “听指令写代码”，很容易导致项目失控。Spec-workflow 通过将严谨的软件工程生命周期（SDLC）“教”给 AI，强制它按照**微型瀑布流（Micro-Waterfall）**的结构化方式进行开发。

### 为什么要引入 Spec-workflow？

在构建复杂的系统、微服务或处理底层数据逻辑时，纯靠自然语言 Prompt 让 AI 直接写代码会暴露明显的缺陷：

- **上下文漂移（Context Drift）：** 随着对话变长，AI 极易忘记最初的业务需求和全局架构约束。
- **架构缺乏一致性：** AI 倾向于给出局部的“补丁式”解决方案，缺乏工程设计思维，容易留下技术债务。
- **黑盒操作与失控：** 很多 Agent 会自动修改大量文件，如果方向跑偏，开发者很难排查和回滚。

Spec-workflow 通过把隐性的上下文变成显性的、机器（和人）均可读的本地规范文件，让 AI 从一个单纯的“高级代码生成器”，变成一个讲纪律、可追溯的“虚拟研发团队”。

## 标准工作流程 (The Micro-Waterfall)

Spec-workflow 通常会在项目的根目录下接管或生成一个 `.spec-workflow`（或类似名称的）目录，通过一系列 Markdown 和结构化文档来编排 AI 的行为。标准的流程包含以下五个阶段：

1. **Steering（项目导向/全局约束）：** 确立全局技术规范。比如强制指定技术栈（如 Python/FastAPI）、设计模式、代码风格或安全限制。这相当于项目的“技术宪法”，AI 在后续所有步骤中都必须高优先级遵守。
2. **Requirements（需求分析）：** AI 会先将你模糊的一句话需求（例如“帮我加个用户鉴权”）转化为结构化的用户故事（User Stories）和可测试的验收标准（Acceptance Criteria）。
3. **Design（系统架构设计）：** 基于需求，AI 接着产出具体的技术架构设计、API 定义、数据表结构变更，有时还会生成 Mermaid 时序图或架构图。
4. **Tasks（任务拆解）：** 将宏大的设计拆解为一系列原子化的、AI 易于理解和执行的步骤清单（Task List）。
5. **Implementation & Approvals（执行与人工审批）：** 这是最关键的一环—— **Human-in-the-loop（人机协同）**。AI 在真正开始“动刀”改代码前，必须将上述的 Spec（规范文档）提交给你审批。只有你确认设计无误，AI 才会顺着任务清单一步步编写和验证代码。

## 常见的技术落地方式

目前，Spec-workflow 的概念在 AI 开发者社区正快速落地，常见的形式包括：

- **MCP Server (Model Context Protocol)：** 例如开源的 `spec-workflow-mcp`，它作为一个标准化的 MCP 服务器，可以把这套工作流能力无缝对接到 Claude Code、Cursor 等支持 MCP 的工具中。
- **IDE 插件扩展：** 比如 VS Code 插件，提供一个可视化控制台，让你在侧边栏直接管理 AI 的规范文档、监控任务进度并进行一键审批。
- **Agentic 协作框架：** 结合子智能体（Sub-agents）能力，编排不同的 AI 角色（如 AI 产品经理、AI 架构师、AI 程序员、AI 测试员）采用接力的方式完成整个 Spec 流程。

简而言之，Spec-workflow 是为了解决 AI 编程的工程化落地而诞生的。它用一套强约束的文档流兜底，确保 AI 产出的代码是可控的、符合预期且具备高可维护性的。
