# 阶段 2：需求定稿

```
现在进入阶段 2：需求定稿。

当前需求：宠物就诊预约管理。

目标：把阶段 1 需求探索中已经确认的内容整理成正式的 `requirements.md`，并通过 `spec-workflow-mcp --dashboard` 完成需求审批流程。

核心要求：

1. 创建或更新 `.spec-workflow/specs/` 下的文件时，优先使用 MCP 暴露的创建/更新工具；如果当前会话没有暴露该工具，则按 `spec_workflow_guide` 创建/更新。
2. 必须使用 `spec-workflow-mcp --dashboard` 完成 requirements 的审批流程。
3. `spec-workflow-mcp --dashboard` 不只是查看状态用，而是用于让用户审查、确认、批准 requirements。
4. 如果当前会话没有暴露可用的 MCP 工具，无法配合 dashboard 完成审批流程，先停止并说明原因。

请先读取：

* `.spec-workflow/steering/product.md`
* `.spec-workflow/steering/tech.md`
* `.spec-workflow/steering/structure.md`
* `AGENTS.md`
* 阶段 1 的需求探索讨论记录

然后创建或更新：

* `.spec-workflow/specs/pet-appointment-management/requirements.md`

`requirements.md` 必须包含：

* 功能名称
* 需求目标
* 用户场景
* 功能性需求
* 非目标
* 输入 / 输出
* 错误场景
* 兼容性要求
* 验收标准
* 范围外事项
* 未确认问题

内容要求：

1. 只写需求，不写设计。
2. 只描述“要做什么”，不要描述“怎么实现”。
3. 不要写 Controller、Service、Repository、DTO、Entity、数据库表、字段、方法名等实现细节。
4. 不要拆 task。
5. 不要写代码。
6. 不要修改业务代码、测试代码、配置文件或 `pom.xml`。
7. 不要扩大阶段 1 已确认的需求范围。
8. 未确认的信息不要脑补，标记为“未确认”。
9. 明确写出非目标和不做事项。
10. 验收标准必须可判断、可测试。

审批要求：

1. requirements 写入后，告知用户启动 dashboard 的命令。
2. 通过 dashboard 等待用户审查 requirements。
3. 如果用户要求修改，只修改 requirements，并继续通过 dashboard 走审批流程。
4. 在 requirements 获得用户批准前，不得进入 design 阶段。
5. 在 requirements 获得用户批准前，不得创建或修改 design.md / tasks.md。
6. 获得批准后，只输出批准结果和文件摘要，然后停止。

禁止修改：

* `src/main/java`
* `src/test/java`
* `src/main/resources`
* `pom.xml`
* `README.md`
* `mvnw`
* `mvnw.cmd`
* 任何业务代码
* 任何测试代码
* 任何构建配置
* `.spec-workflow/specs/` 下除本需求 requirements 文档以外的文件

完成后只输出：

* 使用了哪些 MCP 工具
* 是否使用 `spec-workflow-mcp --dashboard` 完成审批流程
* 创建/修改的文件列表
* requirements 摘要
* 是否包含实现细节：是/否
* 是否修改了禁止文件：是/否
* 审批结果
* 未确认问题列表

完成后停止，等待我审查。
```
