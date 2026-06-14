# AI 辅助开发

## 第 1 阶段：从零启动项目

### 把“我要一个 Java 项目”变成清晰任务

需要掌握：

```text
1. 如何把模糊想法转成明确开发任务
2. 如何描述项目目标、技术栈、边界和不做什么
3. 如何让 AI 先确认需求，而不是直接生成代码
4. 如何识别 AI 过度发挥
5. 如何给 AI 一个可执行的初始任务
```

---

### 建立项目规则文件 AGENTS.md / CLAUDE.md

需要掌握：

```text
1. 项目规则文件的作用
2. 如何声明技术栈、编码规范、测试要求
3. 如何限制 AI 不要擅自引入复杂技术
4. 如何规定每次修改前后必须执行的步骤
5. 如何让不同 AI coding tools 使用同一套项目规则
```

---

### 初始化 Git 与基线提交

需要掌握：

```text
1. 为什么 AI 辅助开发必须先建立 Git 基线
2. git init / git status / git add / git commit 的基本使用
3. 如何创建第一个可回滚状态
4. 如何判断 AI 修改了哪些文件
5. 如何用 git diff 检查 AI 的改动
```

---

### 项目启动流程工具化

需要掌握：

```text
1. 如何把项目启动流程沉淀为命令或 Skill
2. 如何让 AI 按固定流程初始化项目
3. 如何避免每次重复输入长 Prompt
4. 如何把项目规则、Git 初始化、基线测试合并为标准流程
5. 如何判断工具化是否真的提高稳定性
```

---

### AI 开发中的 Git 分支、提交与回滚

需要掌握：

```text
1. 每个功能使用独立分支
2. 每个小任务对应小步提交
3. AI 修改后必须先看 git diff
4. 如何撤销 AI 的错误修改
5. git restore / git reset 的基本使用
6. 如何写清楚 commit message
7. 如何防止 AI 一次性大面积改动
```

---

## 第 2 阶段：基础指令能力

### 从模糊需求到清晰任务

需要掌握：

```text
1. 如何让 AI 追问需求
2. 如何区分业务需求、技术需求、约束条件
3. 如何写清楚输入、输出、异常情况
4. 如何让 AI 输出任务拆解
5. 如何判断任务是否足够小
```

---

### 输出格式控制

需要掌握：

```text
1. 如何要求 AI 使用固定格式输出
2. Markdown 表格、列表、JSON、步骤清单的使用场景
3. 如何让 AI 输出可复制、可执行、可检查的内容
4. 如何避免 AI 输出太散、太长、太模糊
5. 如何让 AI 分离说明、代码、命令和结论
```

---

### Prompt 模板工具化：Commands / Skills

需要掌握：

```text
1. 什么内容适合沉淀为 Command
2. 什么内容适合沉淀为 Skill
3. 如何把高频 Prompt 变成可复用工作流
4. 如何写清楚触发条件、执行步骤、输出格式
5. 如何避免工具模板过度复杂
```

---

### 让 AI 阅读项目结构，并生成项目地图

需要掌握：

```text
1. 如何让 AI 先阅读项目，而不是直接修改代码
2. 如何让 AI 扫描项目目录结构和关键文件
3. 如何让 AI 识别项目入口类、Controller、Service、Store / Repository、DTO、Model、测试目录
4. 如何让 AI 总结当前项目已有功能和接口
5. 如何让 AI 说明“它基于哪些文件做判断”
6. 如何生成 docs/project-map.md 作为可持久化项目地图
7. 如何区分 AGENTS.md 和 project-map.md 的职责
   - AGENTS.md：规定 AI 应该怎么做
   - project-map.md：记录项目现在是什么样
8. 如何在新会话或 AI 重启后，通过读取 project-map.md 恢复项目上下文
9. 如何在项目结构、接口、核心类、请求链路变化后同步更新 project-map.md
10. 如何防止 project-map.md 过期，避免 AI 基于旧项目地图做错误判断
```

---

### 让 AI 追踪一次请求链路，并生成模块级请求链路文档

需要掌握：

```text
1. 如何让 AI 追踪一个请求从 Controller 到 Response 的完整执行路径
2. 如何让 AI 识别 Controller、Service、Store / Repository、DTO、Model 之间的调用关系
3. 如何让 AI 说明请求输入、处理过程、输出结果
4. 如何让 AI 标记一条请求链路涉及的核心文件
5. 如何按照业务模块生成可持久化请求链路文档，例如：
   docs/request-flows/document-api.md
6. 如何把同一业务模块下的相关接口记录在同一个请求链路文档中
7. 如何在新会话或 AI 重启后，通过读取对应的 request flow 文档恢复接口执行链路上下文
8. 如何在新增接口、修改接口、修改 DTO、修改 Service、修改存储逻辑后同步更新对应的请求链路文档
9. 如何区分 docs/project-map.md 和 docs/request-flows/*.md 的职责：
   - docs/project-map.md：记录项目整体结构
   - docs/request-flows/*.md：记录具体业务模块的接口请求链路
10. 如何防止请求链路文档过期，避免 AI 基于旧链路做错误修改
11. 如何让 AI 在修改功能前先判断：
   本次任务会影响哪个业务模块？
   应该读取哪个 request flow 文档？
```

---

### AI 上下文管理

需要掌握：

```text
1. 什么时候给完整文件，什么时候只给片段
2. 如何控制 AI 的输入范围
3. 如何避免长会话上下文污染
4. 如何让 AI 识别过期信息
5. 如何让 AI 先读取相关文件再判断
6. 如何压缩上下文并保留关键决策
7. 什么时候应该开启新会话
```

---

### 让 AI 定位修改点，而不是直接修改

需要掌握：

```text
1. 如何要求 AI 先给修改计划
2. 如何让 AI 说明需要改哪些文件
3. 如何判断修改范围是否合理
4. 如何拒绝 AI 的过度设计方案
5. 如何把“定位问题”和“执行修改”分成两个阶段
```

---

## 第 3 阶段：Plan-Then-Act 与上下文管理

### Plan-Then-Act 与小步实现

需要掌握：

```text
1. Plan-Then-Act 的基本思想
2. 为什么不能让 AI 一上来就写代码
3. 如何要求 AI 先输出执行计划
4. 如何审查 AI 的计划是否合理
5. 如何把功能拆成最小可实现步骤
6. 如何让 AI 一次只完成一个小目标
7. 如何防止 AI 同时改 Controller、Service、测试、配置等过多内容
8. 如何在每一步修改后运行测试
9. 如何确认当前步骤完成后再进入下一步
10. 如何用小步实现降低 AI 出错成本
```

---

### Plan-Then-Act 工具化

需要掌握：

```text
1. 如何把 Plan-Then-Act 写成 Skill 或 Command
2. 如何规定 AI 必须先计划再执行
3. 如何让 AI 在执行前等待确认
4. 如何让 AI 每一步输出当前状态
5. 如何复用同一套计划执行流程
```

---

### 小步提交与可回滚改动

需要掌握：

```text
1. 一个任务完成后立即检查 git diff
2. 一个稳定小功能对应一个 commit
3. 如何用测试结果支撑提交
4. 如何回滚失败尝试
5. 如何避免 AI 修改不可控
6. 如何建立“改动前可恢复，改动后可验证”的习惯
```

### 把 Plan-Then-Act 作为全局开发规则

需要掌握：

```text
1. 如何把 Plan-Then-Act 写入 AGENTS.md / CLAUDE.md
2. 如何规定 AI 修改代码前必须先说明计划
3. 如何区分轻量计划和完整计划
4. 如何判断简单任务是否可以跳过详细计划
5. 如何防止 AI 跳过计划直接修改代码
6. 如何让后续 Spec、TDD、Debug、Review、Refactor 默认继承 Plan-Then-Act
```

---

## 第 4 阶段：Spec Workflow

### 轻量 Spec 结构与 Spec 驱动实现

需要掌握：

```text
1. requirements / design / tasks 的基本结构
2. 什么需求值得写 Spec，什么需求只需要简单任务说明
3. 如何让 AI 从需求生成轻量 Spec
4. 如何审查 Spec 是否过度设计
5. 如何让 requirements 约束功能边界
6. 如何让 design 指导代码结构
7. 如何让 tasks 对应具体代码改动
8. 如何根据 Spec 小步实现一个功能
9. 如何避免实现偏离 requirements
10. 如何在实现完成后反查 Spec 是否满足
```

---

### spec-workflow-mcp 工具化与 MCP 工作流基础

需要掌握：

```text
1. spec-workflow-mcp 的基本用途和适用场景
2. MCP 工具在 AI 辅助开发中的作用：
   通过工具读写结构化状态，而不是只靠聊天上下文
3. spec-workflow-mcp 的项目目录结构：
   .spec-workflow/
   - specs/
   - steering/
   - approvals/
   - archive/
   - templates/
   - user-templates/
4. steering documents 的作用：
   - product steering
   - technical steering
   - structure steering
5. feature spec 的完整生命周期：
   - 创建 spec
   - 编写 requirements
   - 编写 design
   - 拆分 tasks
   - 审批
   - 执行 task
   - 跟踪进度
   - 归档
6. approval workflow 的作用：
   - request approval
   - approve
   - request changes
   - reject
   - revision
7. task management 的作用：
   - pending
   - in-progress
   - completed
   - progress tracking
8. dashboard / VSCode extension 的作用：
   - 查看 specs
   - 查看 steering documents
   - 查看 tasks
   - 处理 approvals
   - 查看 active / archived specs
9. templates / user-templates 的作用：
   - 默认模板
   - 自定义模板
   - 统一 requirements / design / tasks / bug report 格式
10. bug workflow 的作用：
    - 创建 bug report
    - 记录复现步骤
    - 分析 root cause
    - 制定 fix plan
    - 生成 testing requirements
11. archive system 的作用：
    - 归档已完成 spec
    - 保持 active workspace 清晰
    - 必要时恢复 archived spec
12. implementation logs 的作用：
    - 记录 task 实现过程
    - 追踪代码改动统计
    - 支持后续审查和复盘
13. 如何检查 AI 是否真的调用 MCP 工具，而不是口头模拟
14. 如何处理 MCP 状态、Spec 文档、Git diff、测试结果不一致的问题
15. 如何判断什么时候适合使用 spec-workflow-mcp，什么时候只需要轻量任务说明
```

---

### 用 spec-workflow-mcp 完成一个小功能闭环

需要掌握：

```text
1. 如何用 spec-workflow-mcp 从零创建一个小功能 spec
2. 如何在功能开始前检查 steering documents：
   - product steering
   - technical steering
   - structure steering
3. 如何通过 MCP 工具生成并维护 feature spec，而不是只在聊天里口头模拟
4. 如何完成小功能的完整生命周期：
   - 创建 spec
   - 编写 requirements
   - 编写 design
   - 拆分 tasks
   - 提交 approval
   - 根据审批反馈修改
   - 执行 task
   - 更新 task 状态
   - 记录 implementation logs
   - 完成功能验收
   - 归档 spec
5. 如何检查 AI 是否真的调用了 MCP 工具
6. 如何检查 AI 是否正确处理 approval workflow
7. 如何让 AI 一次只执行一个 task
8. 如何让 AI 在 task 开始前更新状态为 in-progress
9. 如何让 AI 在 task 完成后更新状态为 completed
10. 如何在 dashboard / VSCode extension 中追踪功能进度
11. 如何对齐 MCP 状态、Spec 文档、Git diff、测试结果和实际代码完成情况
12. 如何处理 MCP 状态和代码状态不一致的问题
13. 如何判断这个小功能是否适合使用 spec-workflow-mcp
14. 如何判断 spec-workflow-mcp 流程是否稳定、可复用、不过度设计
```

---

### spec-workflow-mcp 中的需求变更管理

需要掌握：

```text
1. 如何判断一个变更属于：
   - requirements 变更
   - design 变更
   - tasks 变更
   - bugfix
   - 新 feature
2. 为什么需求变更时不能直接改代码
3. 如何先读取当前 spec 状态、approval 状态、task 状态和 implementation logs
4. 如何根据变更影响范围更新对应内容：
   - requirements
   - design
   - tasks
   - tests
   - request flow 文档
   - project map
5. 如何通过 approval workflow 处理需求变更：
   - request changes
   - revise
   - approve
   - reject
6. 如何处理已经 completed 的 task 被需求变更影响的情况
7. 如何处理 in-progress task 遇到需求变更的情况
8. 如何记录变更原因、变更影响范围和变更后的验收标准
9. 如何防止 AI 忘记旧需求，避免新需求覆盖旧约束
10. 如何对齐 MCP 状态、Spec 文档、Git diff、测试结果和实际代码状态
11. 如何判断变更完成后是否需要重新归档 spec
12. 如何避免小变更被过度流程化
```

---

## 第 5 阶段：TDD with AI

### 先写测试，不写实现

需要掌握：

```text
1. TDD Red 阶段的目标
2. 如何让 AI 只写失败测试
3. 如何验证测试确实失败
4. 如何避免 AI 偷偷写实现代码
5. 如何让测试表达需求
```

---

### 最小实现让测试通过

需要掌握：

```text
1. TDD Green 阶段的目标
2. 如何让 AI 写最小实现
3. 如何避免 AI 一次性重构
4. 如何验证测试通过
5. 如何判断实现是否超出当前需求
```

---

### 在测试保护下小步重构

需要掌握：

```text
1. TDD Refactor 阶段的目标
2. 如何区分重构和新增功能
3. 如何在测试通过后再整理代码
4. 如何判断重构是否改变行为
5. 如何用测试保护重构安全性
```

---

### TDD Skill 工具化

需要掌握：

```text
1. 如何把 Red / Green / Refactor 固化成 Skill
2. 如何规定每一轮 TDD 的输入和输出
3. 如何防止 AI 跳过 Red 阶段
4. 如何防止 AI 在 Green 阶段过度实现
5. 如何让 AI 每轮都运行测试
```

---

### 使用 spec-workflow-mcp + TDD Skill 的组合实践

需要掌握：

```text
1. Spec Workflow 和 TDD 的分工
2. Spec 管需求、设计、任务
3. TDD 管实现过程和验证
4. 如何一个 task 走一轮 Red / Green / Refactor
5. 如何同步更新 task 状态
6. 如何避免工具之间职责混乱
```

---

### Java 后端测试分层与测试结果阅读

需要掌握：

```text
1. 单元测试的作用
2. Controller 测试的作用
3. Service 测试的作用
4. 集成测试的作用
5. 回归测试的作用
6. 如何让 AI 选择合适测试层级
7. 如何避免所有测试都写成大而全的集成测试
8. 如何阅读测试失败信息
9. 如何理解 expected / actual / assertion error
10. 如何判断测试失败可能来自测试、实现、需求或环境
```

---

### 边界场景、失败场景与回归测试

需要掌握：

```text
1. 为什么 happy path 测试不够
2. 空输入、非法输入、不存在资源的测试
3. 异常返回的测试
4. 边界值测试
5. 重复请求测试
6. 如何让 AI 主动补充失败场景
7. 如何把 bug 转成回归测试
8. 如何防止 AI 为了让测试通过而硬编码、绕过业务逻辑或修改测试逃避问题
```

---

## 第 6 阶段：Debug with AI

### 让 AI 基于日志和错误信息定位问题

需要掌握：

```text
1. 如何提供完整错误信息、操作步骤和复现条件
2. 如何区分编译错误、启动错误、运行时错误、接口错误、配置错误
3. 如何让 AI 先判断问题类型
4. 如何让 AI 给出最可能原因和验证步骤
5. 如何避免 AI 基于半截日志乱猜
6. 如何把确认后的问题转成可验证的修复任务
```

---

### 最小复现与可验证修复

需要掌握：

```text
1. 什么是最小复现
2. 如何让 AI 根据错误构造最小复现路径
3. 如何把 bug 转成可验证的失败用例
4. 如何先复现，再修复
5. 如何用最小修改完成修复
6. 如何确认修复没有破坏旧功能
7. 如何补充回归测试防止问题复发
```

---

## 第 7 阶段：AI 工具工作流集成

### Commands / Skills / Hooks / MCP 的分工

需要掌握：

```text
1. Command 适合短流程和高频操作
2. Skill 适合稳定方法论和复杂工作流
3. Hook 适合自动触发检查、提醒和质量门禁
4. MCP 适合结构化工具调用和状态管理
5. 如何判断一个流程应该使用 Command、Skill、Hook 还是 MCP
6. 如何避免所有东西都工具化
7. 如何避免工具之间职责重叠
```

---

### Hooks 自动化：测试、格式化、提醒

需要掌握：

```text
1. Hooks 的作用
2. 如何在 AI 修改后自动运行测试
3. 如何在提交前自动格式化或检查
4. 如何用 Hooks 提醒 AI 不要跳过关键步骤
5. Hooks 和手动检查的边界
6. 哪些检查适合自动化，哪些检查必须人工确认
```

---

### 工具权限、安全边界与技术栈约束

需要掌握：

```text
1. AI coding tool 的权限风险
2. Shell 命令执行风险
3. 文件读写风险
4. MCP 工具权限风险
5. 如何使用最小权限原则
6. 哪些操作必须人工确认
7. 为什么不能让 AI 随便新增依赖
8. 如何审查 pom.xml / build.gradle 改动
9. 如何要求 AI 说明新增依赖的原因、替代方案和维护成本
10. 如何优先使用现有技术栈解决问题
11. 如何防止 AI 引入不必要的框架、数据库、中间件或复杂架构
12. 如何把技术栈边界写入 AGENTS.md / CLAUDE.md
```

---

### MCP / Skills / Hooks 组合工作流

需要掌握：

```text
1. MCP 负责结构化状态和工具调用
2. Skill 负责行为规范和执行方法
3. Hook 负责自动检查、提醒和质量门禁
4. 如何组合 MCP、Skills、Hooks 完成一个功能
5. 如何处理工具调用失败
6. 如何防止 AI 在工具之间来回混乱
7. 如何检查工具状态、代码状态、测试结果是否一致
```

---

### 工作流冲突处理

需要掌握：

```text
1. 多个规则冲突时如何设置优先级
2. AGENTS.md / CLAUDE.md、Skill、MCP 状态、Hooks 之间冲突时如何处理
3. MCP 状态和实际代码不一致时如何处理
4. Hook 失败时是否允许继续
5. AI 没有调用工具时如何纠正
6. 如何设计降级流程
7. 如何避免工具链过度复杂
```

---

## 第 8 阶段：AI Code Review

### 功能审查与回归审查

需要掌握：

```text
1. 功能是否满足需求
2. 是否破坏已有功能
3. 是否有遗漏场景
4. 是否有无关改动
5. 是否需要补充测试
6. 如何让 AI 先审查，不直接重写
```

---

### Decision / Lesson 驱动的 Review Checklist

需要掌握：

```text
1. 如何从历史决策生成 Review Checklist
2. 如何从踩坑经验生成检查项
3. 如何让 AI 审查时引用项目规则
4. 如何让 Review 越用越准
5. 如何把新问题沉淀回 Lessons Learned
```

---

### Java 后端专项审查

需要掌握：

```text
1. Controller 设计审查
2. DTO / Model 边界审查
3. Service 职责审查
4. 异常处理审查
5. 测试覆盖审查
6. Spring Boot 项目结构审查
7. 可维护性和可扩展性审查
```

---

### AI Diff Review：只审查本次改动

需要掌握：

```text
1. 如何让 AI 只看 git diff
2. 如何避免 AI 泛泛审查整个项目
3. 如何检查本次改动是否过大
4. 如何发现无关格式化和无关重构
5. 如何检查 public contract 是否被破坏
6. 如何根据 diff 生成修改建议
```

---

### Definition of Done：AI 输出验收标准

需要掌握：

```text
1. 如何定义一个任务真正完成
2. 需求是否满足
3. 测试是否通过
4. 文档是否更新
5. 是否有无关改动
6. 是否有安全风险
7. 是否可以回滚
8. 如何让 AI 完成后自检
```

---

### Code Review 工具化

需要掌握：

```text
1. 如何把 Review Checklist 固化为 Skill
2. 如何让 AI 按固定维度审查
3. 如何区分阻塞问题和建议问题
4. 如何生成可执行的整改任务
5. 如何把 Review 流程接入 Hooks 或 MCP
```

---

## 第 9 阶段：重构、文档与长期维护

### 安全小步重构

需要掌握：

```text
1. 重构不等于新增功能
2. 重构前必须有测试保护
3. 如何让 AI 先说明重构目标
4. 如何限制单次重构范围
5. 如何验证重构前后行为一致
6. 如何用 git diff 审查重构风险
```

---

### 重构前后的 Diff 审查

需要掌握：

```text
1. 如何比较重构前后的代码变化
2. 如何识别行为变化
3. 如何发现无意中修改接口语义
4. 如何判断重构是否真的提高可读性
5. 如何决定接受、继续修改或回滚
```

---

### 生成项目文档和 Handoff

需要掌握：

```text
1. 如何让 AI 生成项目说明文档
2. 如何描述项目结构、启动方式、接口列表
3. 如何记录当前功能状态
4. 如何记录未完成事项
5. 如何让新会话或新人快速接手项目
```

---

### Project Memory Handoff 与项目记忆系统治理

需要掌握：

```text
1. 如何整理当前项目上下文
2. 如何区分不同项目记忆文件的职责：
   - AGENTS.md / CLAUDE.md：AI 行为规则
   - docs/project-map.md：项目整体结构地图
   - docs/request-flows/*.md：模块级请求链路
   - .spec-workflow/steering/：长期产品、技术、结构方向
   - Decision Records：关键决策记录
   - Lessons Learned：踩坑经验和改进规则
   - Handoff：当前任务交接状态
3. 如何判断一条信息应该写入哪个文件
4. 如何设计新会话启动时的上下文读取顺序
5. 如何提取关键决策、重要教训和当前任务状态
6. 如何生成新会话交接 Prompt
7. 如何避免交接信息太长、太散或读取过多无关记忆文件
8. 如何在项目结构、接口链路、技术决策、开发规则变化后同步更新对应记忆文件
9. 如何处理不同记忆文件之间的信息不一致
10. 如何让项目自己携带上下文，而不是依赖 AI 会话记忆
```

---

### AI 开发失败案例复盘

需要掌握：

```text
1. 如何分析 AI 为什么做错
2. 如何区分需求错误、上下文错误、工具错误、测试缺失
3. 如何把错误写入 Lessons Learned
4. 如何把重复错误升级为规则
5. 如何把规则同步到 AGENTS.md / Skill / Checklist
6. 如何让一次失败变成长期资产
```

---

## 第 10 阶段：最终工作流固化

### 工作流编排与冲突处理

需要掌握：

```text
1. 需求澄清、Spec、TDD、Debug、Review、Refactor 的完整顺序
2. 什么时候走轻量流程
3. 什么时候走完整 Spec 流程
4. 什么时候使用 TDD
5. 什么时候只做 Review
6. 什么时候需要 Handoff
7. 如何避免流程过重
8. 如何处理工具链冲突
```

---

### MCP / Skills / Hooks 组合项目实践

需要掌握：

```text
1. 用 MCP 管理 Spec 和任务状态
2. 用 Skill 管理 TDD / Review / Debug 行为
3. 用 Hooks 自动运行测试和检查
4. 用项目记忆系统沉淀规则
5. 用 Git 管理风险和回滚
6. 完成一个完整功能开发闭环
```

---

### 最终项目验收与流程固化

需要掌握：

```text
1. 项目功能验收
2. 测试验收
3. 文档验收
4. 代码质量验收
5. AI 工作流验收
6. 工具链验收
7. 复盘整个学习路径
8. 形成个人 AI 辅助开发标准流程
```
