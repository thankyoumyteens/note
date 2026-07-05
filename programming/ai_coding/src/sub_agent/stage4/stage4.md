# 阶段 4：任务拆分

```
现在进入阶段 4：任务拆分。

当前需求：宠物就诊预约管理。

前提：

* `requirements.md` 已通过审批。
* `design.md` 已通过审批。

目标：基于已批准的 `requirements.md` 和 `design.md`，生成 `tasks.md`，把功能拆成小步、可测试、可回滚的任务，并通过 `spec-workflow-mcp --dashboard` 完成任务审批流程。

核心要求：

1. 创建或更新 `.spec-workflow/specs/` 下的文件时，优先使用 MCP 暴露的创建/更新工具；如果当前会话没有暴露该工具，则按 `spec_workflow_guide` 创建/更新。
2. 必须使用 `spec-workflow-mcp --dashboard` 完成 tasks 的审批流程。
3. `spec-workflow-mcp --dashboard` 不只是查看状态用，而是用于让用户审查、确认、批准 tasks。
4. 如果当前会话没有暴露可用的 MCP 工具，无法配合 dashboard 完成审批流程，先停止并说明原因。

请先读取：

* `.spec-workflow/steering/product.md`
* `.spec-workflow/steering/tech.md`
* `.spec-workflow/steering/structure.md`
* `AGENTS.md`
* `.spec-workflow/specs/pet-appointment-management/requirements.md`
* `.spec-workflow/specs/pet-appointment-management/design.md`

然后创建或更新：

* `.spec-workflow/specs/pet-appointment-management/tasks.md`

`tasks.md` 必须包含：

* 任务 ID
* 任务标题
* 任务目标
* 允许修改的文件或目录
* 禁止修改的文件或目录
* 实现说明
* 测试要求
* 完成标准
* 停止条件

任务拆分要求：

1. 每个 task 只解决一个明确问题。
2. 每个 task 必须范围小、可测试、可回滚。
3. 不要把测试、实现、重构混成一个大任务。
4. 能用 TDD 的任务优先拆成 Red / Green / Refactor。
5. 每完成一个 task 后必须停止，等待主 Agent 验收。
6. task 顺序必须符合依赖关系。
7. task 必须严格以已批准的 `requirements.md` 和 `design.md` 为边界。
8. 不要新增 requirements / design 中没有确认的功能。
9. 不要扩大需求范围。
10. 不要写代码。

内容要求：

1. 可以说明每个 task 要修改哪些文件或目录。
2. 可以说明每个 task 要运行哪些测试。
3. 可以说明每个 task 的验收标准。
4. 不要直接修改业务代码、测试代码、配置文件或 `pom.xml`。
5. 不要创建或修改 implementation 文件。
6. 不要执行任何 task。
7. 如果发现 design 中存在无法拆分或存在冲突的地方，标记为“需要用户确认”，不要自行脑补。

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
* `.spec-workflow/specs/` 下除本需求 `tasks.md` 以外的文件

审批要求：

1. `tasks.md` 写入后，告知用户启动 dashboard 的命令。
2. 通过 dashboard 等待用户审查 tasks。
3. 如果用户要求修改，只修改 `tasks.md`，并继续通过 dashboard 走审批流程。
4. 在 tasks 获得用户批准前，不得进入阶段 5。
5. 在 tasks 获得用户批准前，不得执行任何 task。
6. 获得批准后，只输出批准结果和文件摘要，然后停止。

完成后只输出：

* 使用了哪些 MCP 工具
* 如果未使用创建/更新工具，是否按 `spec_workflow_guide` 创建/更新
* 是否使用 `spec-workflow-mcp --dashboard` 完成审批流程
* 创建/修改的文件列表
* tasks 摘要
* 是否包含代码：是/否
* 是否修改了禁止文件：是/否
* 审批结果
* 需要用户确认的问题

完成后停止，等待我确认是否进入阶段 5。
```
