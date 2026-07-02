# 阶段 3：设计评审

```
现在进入阶段 3：设计评审。

当前需求：宠物就诊预约管理。

前提：`requirements.md` 已通过审批。

目标：基于已批准的 `requirements.md` 生成 `design.md`，说明该需求应该如何实现，并通过 `spec-workflow-mcp --dashboard` 完成设计审批流程。

核心要求：

1. 创建或更新 `.spec-workflow/specs/` 下的文件时，优先使用 MCP 暴露的创建/更新工具；如果当前会话没有暴露该工具，则按 `spec_workflow_guide` 创建/更新。
2. 不要绕过 `spec_workflow_guide` 随意创建或修改 `.spec-workflow/specs/` 下的文件。
3. 必须使用 `spec-workflow-mcp --dashboard` 完成 design 的审批流程。
4. 在 `design.md` 获得用户批准前，不得进入阶段 4。
5. 在 `design.md` 获得用户批准前，不得创建或修改 `tasks.md`。
6. 如果当前会话无法使用 dashboard 完成审批流程，先停止并说明原因。

请先读取：

* `.spec-workflow/steering/product.md`
* `.spec-workflow/steering/tech.md`
* `.spec-workflow/steering/structure.md`
* `AGENTS.md`
* `.spec-workflow/specs/pet-appointment-management/requirements.md`

然后创建或更新：

* `.spec-workflow/specs/pet-appointment-management/design.md`

`design.md` 必须包含：

* 设计目标
* 需求边界
* 涉及模块
* 数据模型设计
* API 设计
* 状态流转
* 冲突校验规则
* 错误处理设计
* 兼容性影响
* 测试策略
* 不引入哪些技术
* 不修改哪些边界
* 风险与待确认问题

内容要求：

1. 设计必须严格以已批准的 `requirements.md` 为边界。
2. 不要扩大需求范围。
3. 不要设计未在 requirements 中确认的功能。
4. 可以说明需要新增哪些类、接口、DTO、Repository、Service、Controller，但不要写具体代码。
5. 可以说明需要新增或修改哪些测试，但不要写测试代码。
6. 可以说明数据库结构变化，但不要直接修改数据库脚本。
7. 不要新增外部依赖，除非 `requirements.md` 明确允许。
8. 不要修改业务代码、测试代码、配置文件或 `pom.xml`。
9. 如果发现 requirements 中有无法设计或存在冲突的地方，标记为“需要用户确认”，不要自行脑补。

重点审查：

* 是否过度设计
* 是否新增不必要抽象
* 是否引入不允许的技术
* 是否修改了不该改的 API
* 是否扩大了需求范围
* 是否与 `tech.md` 冲突
* 是否与 `structure.md` 冲突
* 是否影响现有 owner、pet、vet、visit 接口行为

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
* `.spec-workflow/specs/` 下除本需求 `design.md` 以外的文件

审批要求：

1. `design.md` 写入后，使用 `spec-workflow-mcp --dashboard` 让用户审查。
2. 如果用户要求修改，只修改 `design.md`。
3. 修改后继续通过 dashboard 完成审批流程。
4. 在 design 获得批准前，不得进入阶段 4。
5. 获得批准后停止，等待我确认是否进入阶段 4。

完成后只输出：

* 使用了哪些 MCP 工具
* 如果未使用创建/更新工具，是否按 `spec_workflow_guide` 创建/更新
* 是否使用 `spec-workflow-mcp --dashboard` 完成审批流程
* 创建/修改的文件列表
* design 摘要
* 是否包含代码：是/否
* 是否修改了禁止文件：是/否
* 审批结果
* 需要用户确认的问题

完成后停止。
```
