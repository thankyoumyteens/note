# 第 1 部分：从零启动 AI 辅助开发项目

## 1. 把“我要一个 Java 项目”变成清晰任务

需要掌握：

1. 如何把模糊想法转成明确开发任务
2. 如何描述项目目标、技术栈、边界和不做什么
3. 如何让 AI 先确认需求，而不是直接生成代码
4. 如何识别 AI 过度发挥
5. 如何给 AI 一个可执行的初始任务
6. 如何把业务目标、验收标准和实现约束分开描述
7. 如何要求 AI 明确“本次不做什么”

## 2. 建立多工具项目规则文件：AGENTS.md / CLAUDE.md / Copilot Instructions

需要掌握：

1. AGENTS.md、CLAUDE.md、Copilot instructions 的作用边界
2. 哪些工具默认读取 AGENTS.md，哪些工具默认读取 CLAUDE.md
3. 如何用 CLAUDE.md import AGENTS.md，避免重复维护规则
4. 如何声明技术栈、编码规范、测试要求、禁止事项
5. 如何限制 AI 不要擅自引入复杂技术
6. 如何规定每次修改前后必须执行的步骤
7. 如何让不同 AI coding tools 尽量复用同一套项目规则
8. 如何设计“主规则文件 + 工具适配文件”的结构
9. 如何避免多份规则文件互相冲突
10. 如何定期检查规则文件是否过期

建议理解：

```text
AGENTS.md              → 跨工具主规则候选文件
CLAUDE.md              → Claude Code 项目记忆入口
.github/copilot-*.md   → GitHub Copilot 专用说明
工具私有配置文件        → 只放该工具必须知道的适配规则
```

## 3. 初始化 Git 与基线提交

需要掌握：

1. 为什么 AI 辅助开发必须先建立 Git 基线
2. git init / git status / git add / git commit 的基本使用
3. 如何创建第一个可回滚状态
4. 如何判断 AI 修改了哪些文件
5. 如何用 git diff 检查 AI 的改动
6. 为什么没有 Git 基线时不应该让 AI 大范围改代码

## 4. AI 开发中的 Git 分支、提交与回滚

需要掌握：

1. 每个功能使用独立分支
2. 每个小任务对应小步提交
3. AI 修改后必须先看 git diff
4. 如何撤销 AI 的错误修改
5. git restore / git reset 的基本使用
6. 如何写清楚 commit message
7. 如何防止 AI 一次性大面积改动
8. 如何区分“回滚当前文件”“回滚当前提交”“重置整个分支”
9. 如何避免把 AI 的临时尝试混进稳定提交

---

# 第 2 部分：基础指令能力

## 5. 从模糊需求到清晰任务

需要掌握：

1. 如何让 AI 追问需求
2. 如何区分业务需求、技术需求、约束条件
3. 如何写清楚输入、输出、异常情况
4. 如何让 AI 输出任务拆解
5. 如何判断任务是否足够小
6. 如何让 AI 明确验收标准
7. 如何避免“看起来完成，实际不可验收”的任务描述

## 6. Prompt 模板工具化：Skills / Commands / Reusable Instructions

需要掌握：

1. 什么内容适合沉淀为 Skill
2. 什么内容适合保留为 Command
3. 为什么复杂流程优先用 Skill，而不是长 Prompt
4. 如何写清楚 Skill 的触发条件、执行步骤、输入、输出、停止条件
5. 如何让 Skill 支持 Review、Debug、TDD、Handoff 等稳定工作流
6. 如何避免 Skill 过度复杂、过度自动化
7. 如何处理不同工具对 Command / Skill 支持不一致的问题
8. 如何把高频 Prompt 变成可复用工作流
9. 如何避免模板替代思考

建议理解：

```text
Command  → 快捷入口、短流程、兼容机制
Skill    → 稳定方法论、复杂流程、可复用工作流
Prompt   → 临时任务说明，不适合长期复用
```

## 7. 让 AI 阅读项目结构，并生成项目地图

需要掌握：

1. 如何让 AI 先阅读项目，而不是直接修改代码
2. 如何让 AI 扫描项目目录结构和关键文件
3. 如何让 AI 识别项目入口类、Controller、Service、Store / Repository、DTO、Model、测试目录
4. 如何让 AI 总结当前项目已有功能和接口
5. 如何让 AI 说明“它基于哪些文件做判断”
6. 如何生成 docs/project-map.md 作为可持久化项目地图
7. 如何区分 AGENTS.md / CLAUDE.md 和 project-map.md 的职责
   - AGENTS.md / CLAUDE.md：规定 AI 应该怎么做
   - project-map.md：记录项目现在是什么样
8. 如何在新会话或 AI 重启后，通过读取 project-map.md 恢复项目上下文
9. 如何在项目结构、接口、核心类、请求链路变化后同步更新 project-map.md
10. 如何防止 project-map.md 过期，避免 AI 基于旧项目地图做错误判断
11. 如何让 AI 在修改前判断 project-map.md 是否可能已经过期

## 8. 让 AI 追踪一次请求链路，并生成模块级请求链路文档

需要掌握：

1. 如何让 AI 追踪一个请求从 Controller 到 Response 的完整执行路径
2. 如何让 AI 识别 Controller、Service、Store / Repository、DTO、Model 之间的调用关系
3. 如何让 AI 说明请求输入、处理过程、输出结果
4. 如何让 AI 标记一条请求链路涉及的核心文件
5. 如何按照业务模块生成可持久化请求链路文档，例如：docs/request-flows/document-api.md
6. 如何把同一业务模块下的相关接口记录在同一个请求链路文档中
7. 如何在新会话或 AI 重启后，通过读取对应的 request flow 文档恢复接口执行链路上下文
8. 如何在新增接口、修改接口、修改 DTO、修改 Service、修改存储逻辑后同步更新对应的请求链路文档
9. 如何区分 docs/project-map.md 和 docs/request-flows/\*.md 的职责：
   - docs/project-map.md：记录项目整体结构
   - docs/request-flows/\*.md：记录具体业务模块的接口请求链路
10. 如何防止请求链路文档过期，避免 AI 基于旧链路做错误修改
11. 如何让 AI 在修改功能前先判断：
    - 本次任务会影响哪个业务模块？
    - 应该读取哪个 request flow 文档？

## 9. AI 上下文管理

需要掌握：

1. 什么时候给完整文件，什么时候只给片段
2. 如何控制 AI 的输入范围
3. 如何避免长会话上下文污染
4. 如何让 AI 识别过期信息
5. 如何让 AI 先读取相关文件再判断
6. 如何压缩上下文并保留关键决策
7. 什么时候应该开启新会话
8. 如何利用项目规则文件降低反复贴上下文的成本
9. 如何利用 Skills、MCP、Subagents、Code Intelligence 分担上下文压力
10. 如何判断“上下文太多”导致 AI 判断质量下降

## 10. 让 AI 定位修改点，而不是直接修改

需要掌握：

1. 如何要求 AI 先给修改计划
2. 如何让 AI 说明需要改哪些文件
3. 如何判断修改范围是否合理
4. 如何拒绝 AI 的过度设计方案
5. 如何把“定位问题”和“执行修改”分成两个阶段
6. 如何要求 AI 给出“预计不需要修改的文件”
7. 如何防止 AI 在定位阶段直接写代码

---

# 第 3 部分：Plan-Then-Act 与小步实现

## 11. Plan-Then-Act 与小步实现

需要掌握：

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
11. 如何区分轻量计划和完整计划
12. 如何避免计划本身过度复杂

## 12. 小步提交与可回滚改动

需要掌握：

1. 一个任务完成后立即检查 git diff
2. 一个稳定小功能对应一个 commit
3. 如何用测试结果支撑提交
4. 如何回滚失败尝试
5. 如何避免 AI 修改不可控
6. 如何建立“改动前可恢复，改动后可验证”的习惯
7. 如何避免把多个无关修改混进一个 commit
8. 如何在 commit message 中说明 AI 辅助修改的范围

## 13. Plan-Then-Act 工具化

需要掌握：

1. 如何把 Plan-Then-Act 写成 Skill 或 Command
2. 如何规定 AI 必须先计划再执行
3. 如何让 AI 在执行前等待确认
4. 如何让 AI 每一步输出当前状态
5. 如何复用同一套计划执行流程
6. 如何规定 AI 完成一步后必须停止
7. 如何让 Hook 或规则文件提醒 AI 不要跳过计划

## 14. 把 Plan-Then-Act 作为全局开发规则

需要掌握：

1. 如何把 Plan-Then-Act 写入 AGENTS.md / CLAUDE.md
2. 如何规定 AI 修改代码前必须先说明计划
3. 如何区分轻量计划和完整计划
4. 如何判断简单任务是否可以跳过详细计划
5. 如何防止 AI 跳过计划直接修改代码
6. 如何让后续 Spec、TDD、Debug、Review、Refactor 默认继承 Plan-Then-Act
7. 如何处理“用户明确要求直接改”和“项目规则要求先计划”的冲突

---

# 第 4 部分：Spec Workflow

## 15. 轻量 Spec 结构与 Spec 驱动实现

需要掌握：

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
11. 如何判断 Spec 需要更新还是实现需要修正

## 16. spec-workflow-mcp 工具化与 MCP 工作流基础

需要掌握：

1. spec-workflow-mcp 的基本用途和适用场景
2. MCP 工具在 AI 辅助开发中的作用：通过工具读写结构化状态，而不是只靠聊天上下文
3. spec-workflow-mcp 的项目目录结构：
   - .spec-workflow/
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

## 17. 用 spec-workflow-mcp 完成一个小功能闭环

需要掌握：

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

## 18. spec-workflow-mcp 中的需求变更管理

需要掌握：

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

## 19. spec-workflow-mcp 的适用边界与降级策略

需要掌握：

1. 什么任务值得使用 spec-workflow-mcp
2. 什么任务只需要轻量任务说明
3. 小 bugfix 是否需要完整 spec
4. 如何避免小变更被流程化拖慢
5. MCP 不可用时如何降级到 Markdown Spec
6. Dashboard 状态、Spec 文档、Git diff、测试结果不一致时以什么为准
7. 如何防止 AI 口头模拟 MCP 调用
8. 如何做最小闭环，而不是追求流程完整度
9. 如何识别“工具流程正确，但功能没有真正完成”的情况
10. 如何把 spec-workflow-mcp 当作状态工具，而不是让它替代工程判断

---

# 第 5 部分：TDD with AI

## 20. 先写测试，不写实现

需要掌握：

1. TDD Red 阶段的目标
2. 如何让 AI 只写失败测试
3. 如何验证测试确实失败
4. 如何避免 AI 偷偷写实现代码
5. 如何让测试表达需求
6. 如何让 AI 解释测试为什么应该失败
7. 如何确认失败原因来自功能缺失，而不是测试写错或环境问题

## 21. 最小实现让测试通过

需要掌握：

1. TDD Green 阶段的目标
2. 如何让 AI 写最小实现
3. 如何避免 AI 一次性重构
4. 如何验证测试通过
5. 如何判断实现是否超出当前需求
6. 如何判断最小实现是否只是投机实现
7. 如何防止 AI 用硬编码、固定返回值或 return null 绕过测试

## 22. 在测试保护下小步重构

需要掌握：

1. TDD Refactor 阶段的目标
2. 如何区分重构和新增功能
3. 如何在测试通过后再整理代码
4. 如何判断重构是否改变行为
5. 如何用测试保护重构安全性
6. 如何限制一次重构只解决一个明确问题
7. 如何在重构后重新运行相关测试和回归测试

## 23. TDD Skill 工具化

需要掌握：

1. 如何把 Red / Green / Refactor 固化成 Skill
2. 如何规定每一轮 TDD 的输入和输出
3. 如何防止 AI 跳过 Red 阶段
4. 如何防止 AI 在 Green 阶段过度实现
5. 如何让 AI 每轮都运行测试
6. 如何要求每轮结束后停止，等待用户确认
7. 如何记录每轮的测试结果、修改范围和下一步建议

## 24. 使用 spec-workflow-mcp + TDD Skill 的组合实践

需要掌握：

1. Spec Workflow 和 TDD 的分工
2. Spec 管需求、设计、任务
3. TDD 管实现过程和验证
4. 如何一个 task 走一轮 Red / Green / Refactor
5. 如何同步更新 task 状态
6. 如何避免工具之间职责混乱
7. 如何确保每个 task 开始前先更新为 in-progress
8. 如何确保每个 task 完成后再更新为 completed
9. 如何确保每个 task 都独立走 Red / Green / Refactor，而不是多个 task 混在一起做

## 25. Java 后端测试分层与测试结果阅读

需要掌握：

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
11. 如何判断 MockMvc、Service test、Repository test 的适用边界
12. 如何防止测试层级错位导致测试脆弱

## 26. 边界场景、失败场景与回归测试

需要掌握：

1. 为什么 happy path 测试不够
2. 空输入、非法输入、不存在资源的测试
3. 异常返回的测试
4. 边界值测试
5. 重复请求测试
6. 如何让 AI 主动补充失败场景
7. 如何把 bug 转成回归测试
8. 如何防止 AI 为了让测试通过而硬编码、绕过业务逻辑或修改测试逃避问题
9. 如何把线上问题、历史 bug、踩坑经验转成可长期保留的测试用例

## 27. AI TDD 反作弊：测试质量与最小实现边界

需要掌握：

1. 如何判断测试是否真的表达业务行为
2. 如何识别“只测字段 / 方法存在”的伪测试
3. 如何识别“只测 Controller 结构，不测业务逻辑”的低质量测试
4. 如何识别“为了测试而测试”的脆弱测试
5. 如何防止 Green 阶段用 return null、硬编码、固定返回值绕过测试
6. 如何要求 AI 解释测试为什么会失败
7. 如何要求 AI 解释最小实现为什么不是投机实现
8. 如何在 Refactor 前确认行为测试已经覆盖关键路径
9. 如何规定 AI 不得修改 Red 阶段已经确认的测试，除非用户批准
10. 如何通过 Review Checklist 检查测试是否真的保护业务行为

---

# 第 6 部分：Debug with AI

## 28. 让 AI 基于日志和错误信息定位问题

需要掌握：

1. 如何提供完整错误信息、操作步骤和复现条件
2. 如何区分编译错误、启动错误、运行时错误、接口错误、配置错误
3. 如何让 AI 先判断问题类型
4. 如何让 AI 给出最可能原因和验证步骤
5. 如何避免 AI 基于半截日志乱猜
6. 如何把确认后的问题转成可验证的修复任务
7. 如何要求 AI 明确“当前证据支持什么，不支持什么”
8. 如何避免 AI 直接给大改方案

## 29. 最小复现与可验证修复

需要掌握：

1. 什么是最小复现
2. 如何让 AI 根据错误构造最小复现路径
3. 如何把 bug 转成可验证的失败用例
4. 如何先复现，再修复
5. 如何用最小修改完成修复
6. 如何确认修复没有破坏旧功能
7. 如何补充回归测试防止问题复发
8. 如何在修复后更新 Lessons Learned 或 request flow 文档

---

# 第 7 部分：AI 工具工作流集成

## 30. Commands / Skills / Hooks / MCP 的分工

需要掌握：

1. Command 适合短流程、高频入口和兼容机制
2. Skill 适合稳定方法论和复杂工作流
3. Hook 适合自动触发检查、提醒、拦截和质量门禁
4. MCP 适合结构化工具调用、外部系统集成和状态管理
5. 如何判断一个流程应该使用 Command、Skill、Hook 还是 MCP
6. 如何避免所有东西都工具化
7. 如何避免工具之间职责重叠
8. 如何判断工具层是否已经比任务本身更复杂

建议理解：

```text
Command  → 入口
Skill    → 方法
Hook     → 自动检查 / 拦截
MCP      → 工具调用 / 状态管理
```

## 31. Hooks 自动化：测试、格式化、提醒、权限拦截与质量门禁

需要掌握：

1. Hooks 的触发时机和生命周期
2. 如何在 AI 修改后自动运行测试
3. 如何在提交前自动格式化或检查
4. 如何用 Hooks 阻止危险命令或越界操作
5. 如何用 Hooks 提醒 AI 不要跳过 Spec / TDD / Review
6. async hooks、HTTP hooks、prompt hooks、MCP tool hooks 的基本概念
7. 哪些检查适合自动化，哪些检查必须人工确认
8. Hook 失败时是否允许继续
9. 如何避免 Hooks 过多导致开发流程变重
10. 如何设计 Hook 的失败提示，让 AI 能根据失败原因修复

## 32. 工具权限、安全边界与技术栈约束

需要掌握：

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
13. AI coding tool 的权限模式：只读、询问、自动、危险模式
14. 哪些命令永远不能自动执行
15. 哪些文件修改必须人工确认
16. 如何审查 AI 对权限的解释是否可信
17. 如何限制 AI 只能改当前 task 相关文件
18. 如何禁止 AI 修改 build、CI、部署、密钥、权限相关文件
19. 如何在 Hooks / settings / rules 中落实权限边界

## 33. Claude Code / Codex 生态中的扩展机制总览

需要掌握：

1. CLAUDE.md / AGENTS.md：项目规则和长期上下文
2. Skills：可复用工作流
3. Commands：交互入口、快捷操作或兼容机制
4. Hooks：自动检查、提醒、权限拦截、质量门禁
5. MCP：外部工具、结构化状态、系统集成
6. Subagents：隔离上下文、专项任务、并行探索
7. Plugins：打包 Skills、Hooks、Subagents、MCP servers 等能力
8. Code Intelligence：让 AI 理解代码引用、定义、调用关系
9. Agent Teams：多个专用 agent 分工协作的组织方式
10. 如何避免扩展机制堆叠过度
11. 如何判断一种工具能力是“必须使用”还是“锦上添花”

## 34. Subagents：隔离上下文与小步执行

需要掌握：

1. Sub Agent 的作用
2. 为什么复杂任务不能让一个 Agent 从头做到尾
3. 主 Agent 负责规划、分派和验收
4. Sub Agent 只负责当前小任务执行
5. 如何限制 Sub Agent 的修改范围
6. 如何防止 Sub Agent 扩展需求
7. 如何防止 Sub Agent 修改未授权文件
8. 如何要求 Sub Agent 完成后停止
9. 如何让主 Agent 基于 git diff、测试结果和任务状态验收
10. 如何在最终工作流中使用主 Agent / Sub Agent 分工

建议理解：

```text
主 Agent  → 规划、拆分、分派、验收、记录
Sub Agent → 只执行当前小任务，完成后停止
```

## 35. MCP / Skills / Hooks 组合工作流

需要掌握：

1. MCP 负责结构化状态和工具调用
2. Skill 负责行为规范和执行方法
3. Hook 负责自动检查、提醒和质量门禁
4. 如何组合 MCP、Skills、Hooks 完成一个功能
5. 如何处理工具调用失败
6. 如何防止 AI 在工具之间来回混乱
7. 如何检查工具状态、代码状态、测试结果是否一致
8. 如何定义组合工作流中的主流程和降级流程
9. 如何避免“工具都调用了，但任务没完成”

## 36. 工作流冲突处理

需要掌握：

1. 多个规则冲突时如何设置优先级
2. AGENTS.md / CLAUDE.md、Skill、MCP 状态、Hooks 之间冲突时如何处理
3. MCP 状态和实际代码不一致时如何处理
4. Hook 失败时是否允许继续
5. AI 没有调用工具时如何纠正
6. 如何设计降级流程
7. 如何避免工具链过度复杂
8. 如何处理用户临时指令和项目长期规则冲突
9. 如何判断“规则太多导致 AI 执行质量下降”

## 37. 主流 AI Coding Tools 差异与迁移策略

需要掌握：

1. Claude Code、Codex、GitHub Copilot、Cursor、Kiro 的定位差异
2. 哪些配置文件可以跨工具复用
3. 哪些配置是工具私有能力
4. AGENTS.md、CLAUDE.md、Copilot instructions 的兼容关系
5. Skill、Command、Hook、MCP 在不同工具中的支持差异
6. 如何避免课程绑定单一工具
7. 如何设计“方法论稳定、工具层可替换”的项目工作流
8. 如何在更换工具时保留项目规则、文档、测试和工作流资产
9. 如何判断新工具是否值得迁移
10. 如何避免为了尝鲜工具而破坏已有稳定流程

---

# 第 8 部分：AI Code Review

## 38. 功能审查与回归审查

需要掌握：

1. 功能是否满足需求
2. 是否破坏已有功能
3. 是否有遗漏场景
4. 是否有无关改动
5. 是否需要补充测试
6. 如何让 AI 先审查，不直接重写
7. 如何区分阻塞问题、建议问题和风格问题
8. 如何要求 AI 基于证据审查，而不是泛泛而谈

## 39. Decision / Lesson 驱动的 Review Checklist

需要掌握：

1. 如何从历史决策生成 Review Checklist
2. 如何从踩坑经验生成检查项
3. 如何让 AI 审查时引用项目规则
4. 如何让 Review 越用越准
5. 如何把新问题沉淀回 Lessons Learned
6. 如何把重复出现的问题升级为 AGENTS.md / Skill / Hook 规则
7. 如何防止 Checklist 越写越长，最后没人执行

## 40. Java 后端专项审查

需要掌握：

1. Controller 设计审查
2. DTO / Model 边界审查
3. Service 职责审查
4. 异常处理审查
5. 测试覆盖审查
6. Spring Boot 项目结构审查
7. 可维护性和可扩展性审查
8. 事务边界审查
9. 参数校验审查
10. 日志与错误信息审查
11. 依赖新增与技术栈边界审查

## 41. AI Diff Review：只审查本次改动

需要掌握：

1. 如何让 AI 只看 git diff
2. 如何避免 AI 泛泛审查整个项目
3. 如何检查本次改动是否过大
4. 如何发现无关格式化和无关重构
5. 如何检查 public contract 是否被破坏
6. 如何根据 diff 生成修改建议
7. 如何让 AI 区分“本次改动造成的问题”和“历史遗留问题”
8. 如何用 diff review 判断是否应该拆分提交

## 42. Definition of Done：AI 输出验收标准

需要掌握：

1. 如何定义一个任务真正完成
2. 需求是否满足
3. 测试是否通过
4. 文档是否更新
5. 是否有无关改动
6. 是否有安全风险
7. 是否可以回滚
8. 如何让 AI 完成后自检
9. 如何判断任务是否达到“可提交”状态
10. 如何避免 AI 用“看起来没问题”代替验收证据

## 43. Code Review 工具化

需要掌握：

1. 如何把 Review Checklist 固化为 Skill
2. 如何让 AI 按固定维度审查
3. 如何区分阻塞问题和建议问题
4. 如何生成可执行的整改任务
5. 如何把 Review 流程接入 Hooks 或 MCP
6. 如何让 Review 输出保持简洁、可执行、可追踪
7. 如何避免 Review Skill 变成空泛模板

---

# 第 9 部分：重构、文档与长期维护

## 44. 安全小步重构

需要掌握：

1. 重构不等于新增功能
2. 重构前必须有测试保护
3. 如何让 AI 先说明重构目标
4. 如何限制单次重构范围
5. 如何验证重构前后行为一致
6. 如何用 git diff 审查重构风险
7. 如何避免 AI 借重构名义改业务逻辑
8. 如何判断某次重构是否值得做

## 45. 重构前后的 Diff 审查

需要掌握：

1. 如何比较重构前后的代码变化
2. 如何识别行为变化
3. 如何发现无意中修改接口语义
4. 如何判断重构是否真的提高可读性
5. 如何决定接受、继续修改或回滚
6. 如何用测试结果和 diff 共同判断重构安全性
7. 如何发现“无关格式化掩盖真实改动”

## 46. 生成项目文档和 Handoff

需要掌握：

1. 如何让 AI 生成项目说明文档
2. 如何描述项目结构、启动方式、接口列表
3. 如何记录当前功能状态
4. 如何记录未完成事项
5. 如何让新会话或新人快速接手项目
6. 如何让 Handoff 包含当前分支、最近 commit、未提交 diff、测试状态
7. 如何避免 Handoff 写成流水账

## 47. Project Memory Handoff 与项目记忆系统治理

需要掌握：

1. 如何整理当前项目上下文
2. 如何区分不同项目记忆文件的职责：
   - AGENTS.md / CLAUDE.md：AI 行为规则
   - docs/project-map.md：项目整体结构地图
   - docs/request-flows/\*.md：模块级请求链路
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

## 48. 显式项目记忆 vs 工具自动记忆

需要掌握：

1. 显式项目记忆：AGENTS.md、CLAUDE.md、project-map、request-flows、steering、ADR、Lessons、Handoff
2. 工具自动记忆：Claude Code Auto Memory 等
3. 哪些信息必须写入项目文件，而不能只依赖工具记忆
4. 哪些信息可以交给工具自动记忆
5. 如何处理自动记忆和项目文件不一致
6. 如何防止记忆膨胀、上下文污染和过期规则
7. 如何设计新会话启动时的读取顺序
8. 如何让项目自己携带上下文，而不是依赖某个 AI 账号或会话
9. 如何定期清理或压缩过期记忆
10. 如何判断工具记忆是否已经影响 AI 判断质量

## 49. AI 开发失败案例复盘

需要掌握：

1. 如何分析 AI 为什么做错
2. 如何区分需求错误、上下文错误、工具错误、测试缺失
3. 如何把错误写入 Lessons Learned
4. 如何把重复错误升级为规则
5. 如何把规则同步到 AGENTS.md / Skill / Checklist
6. 如何让一次失败变成长期资产
7. 如何判断失败原因是模型能力问题、提示问题、流程问题还是工具问题
8. 如何从失败案例中生成可执行的预防规则

---

# 第 10 部分：最终工作流固化

## 50. 分级工作流固化

需要掌握：

1. 为什么不能所有任务都走完整流程
2. 如何区分轻量任务、标准功能、复杂功能
3. 如何根据风险选择流程级别
4. 如何避免流程过重
5. 如何避免流程过轻导致质量失控
6. 如何让 AI 在开始前说明本次使用哪个流程级别
7. 如何在任务中途升级或降级流程

### Level 1：轻量任务流程

适用：小修改、小 bug、文档、小重构。

```text
明确任务
    ↓
定位修改点
    ↓
小步修改
    ↓
测试 / 验证
    ↓
diff review
    ↓
commit
```

需要掌握：

1. 什么任务可以走轻量流程
2. 轻量流程中哪些步骤不能省略
3. 如何防止小任务被过度流程化
4. 如何确保轻量流程仍然可验证、可回滚

### Level 2：标准功能流程

适用：普通业务功能。

```text
需求澄清
    ↓
轻量 Spec
    ↓
tasks
    ↓
每个 task 小步实现
    ↓
测试
    ↓
review
    ↓
文档同步
    ↓
commit
```

需要掌握：

1. 什么功能适合标准流程
2. 如何控制 Spec 的轻重
3. 如何拆分 task
4. 如何在每个 task 后做最小验证
5. 如何防止标准流程滑向完整重流程

### Level 3：完整 Spec + TDD + MCP 流程

适用：复杂功能、多模块变更、长期维护功能。

```text
steering 校准
    ↓
requirements
    ↓
design
    ↓
tasks
    ↓
approval
    ↓
task in-progress
    ↓
Red
    ↓
Green
    ↓
Refactor
    ↓
task completed
    ↓
implementation logs
    ↓
review
    ↓
archive
```

需要掌握：

1. 什么任务必须走完整流程
2. 如何把 spec-workflow-mcp 和 TDD Skill 组合起来
3. 如何确保每个 task 独立闭环
4. 如何确保 approval、task 状态、测试、diff、文档一致
5. 如何在复杂流程中避免 AI 混淆职责

## 51. 工作流编排与冲突处理

需要掌握：

1. 需求澄清、Spec、TDD、Debug、Review、Refactor 的完整顺序
2. 什么时候走轻量流程
3. 什么时候走标准功能流程
4. 什么时候走完整 Spec 流程
5. 什么时候使用 TDD
6. 什么时候只做 Review
7. 什么时候需要 Handoff
8. 如何避免流程过重
9. 如何处理工具链冲突
10. 如何处理 AI 跳步、越界、遗漏状态更新的问题
11. 如何设计“失败后回到哪一步”的恢复规则

## 52. 主 Agent / Sub Agent 分工工作流：Plan broadly, execute narrowly

核心原则：Plan broadly, execute narrowly.

也就是：

1. 前期需求和方案可以充分讨论；
2. 实际执行必须小步、可测试、可回滚。

### 阶段 0：项目级上下文校准

目标：让 AI 先理解当前项目的长期边界，避免后续需求讨论和实现阶段偏离项目路线。

需要读取或校准：

```text
.spec-workflow/steering/product.md
.spec-workflow/steering/tech.md
.spec-workflow/steering/structure.md
AGENTS.md
CLAUDE.md
WORKFLOW.md
docs/decisions/
docs/lessons/
```

重点确认：

```text
项目目标是什么
当前技术栈是什么
哪些技术明确不引入
当前架构边界是什么
项目目录结构如何组织
历史上 AI 犯过哪些错误
哪些规则已经稳定沉淀
```

输出：

```text
项目上下文摘要
当前约束列表
本次需求讨论必须遵守的边界
```

### 阶段 1：需求探索与反复讨论

目标：人和 AI 反复讨论，把模糊想法逐步变成清晰需求。

这一阶段不急着写正式 `requirements.md`，重点是让 AI 不断追问、质疑、补全遗漏因素。

AI 应该持续 grill me，围绕以下问题反复追问：

```text
这个需求真正解决什么问题？
目标用户是谁？
用户会在什么场景下使用？
最小可用版本是什么？
哪些情况必须支持？
哪些情况明确不支持？
输入是什么？
输出是什么？
失败时如何处理？
是否影响已有接口？
是否影响已有测试？
是否需要兼容旧行为？
是否允许新增依赖？
是否允许修改数据结构？
是否允许修改 API 响应格式？
是否需要权限、安全、审计、日志？
是否存在性能或并发要求？
哪些设计会过度？
哪些东西这次明确不做？
如何判断这个需求完成？
```

人的职责：

```text
回答 AI 的问题
纠正 AI 的误解
删除过度设计
补充真实业务约束
明确取舍
决定哪些做、哪些不做
```

AI 的职责：

```text
持续追问
发现歧义
发现遗漏场景
指出潜在冲突
把讨论结果整理成候选需求
不要直接写代码
不要直接进入设计
不要替人做最终取舍
```

本阶段输出：

```text
需求讨论记录
已确认事项
未确认问题
明确不做事项
风险和待决策点
```

停止条件：

```text
目标、边界、非目标、验收标准已经足够清晰；
没有重大未确认问题；
人明确同意进入需求定稿阶段。
```

### 阶段 2：需求定稿

目标：把阶段 1 的讨论结果整理成正式 feature-level requirements。

产出：

```text
requirements.md
```

内容应包括：

```text
Feature name
Goal
User scenarios
Functional requirements
Non-goals
Input / output
Error cases
Compatibility requirements
Acceptance criteria
Out of scope
```

要求：

```text
只描述要做什么
不写具体实现方案
不写代码
不拆 task
不提前决定技术细节
```

验收标准：

```text
人可以根据 requirements.md 判断功能是否完成
AI 不能再靠脑补扩展需求
后续 design.md 必须以 requirements.md 为边界
```

### 阶段 3：设计评审

目标：让 AI 基于 requirements.md 提出实现设计，然后由人审查是否合理、是否过度设计。

产出：

```text
design.md
```

设计内容包括：

```text
涉及哪些模块
是否需要新增类或方法
API 行为如何变化
错误处理方式
测试策略
兼容性影响
不引入哪些技术
不修改哪些边界
```

人需要重点审查：

```text
是否过度设计
是否新增不必要抽象
是否引入不允许的技术
是否修改了不该改的 API
是否扩大了需求范围
是否和 tech.md 冲突
是否和 structure.md 冲突
```

本阶段明确不做：

```text
不写代码
不修改测试
不新增依赖
不直接执行实现
```

停止条件：

```text
design.md 被人确认；
所有关键技术取舍已经明确；
不做事项已经写清楚。
```

### 阶段 4：任务拆分

目标：把已确认的 requirements.md 和 design.md 拆成小任务。

产出：

```text
tasks.md
```

每个 task 必须满足：

```text
目标清晰
范围小
可测试
可回滚
有完成标准
有允许修改范围
有禁止修改范围
```

推荐 task 格式：

```text
Task ID
Task title
Goal
Allowed files
Forbidden files
Implementation notes
Test requirements
Completion criteria
Stop condition
```

拆分原则：

```text
一个 task 只解决一个明确问题
不要把测试、实现、重构混成一大步
能用 TDD 的任务优先 Red / Green / Refactor
每完成一个 task 后必须停止
```

### 阶段 5：分 task 执行

目标：主 Agent 选择当前第一个未完成 task，把它交给 Sub Agent 执行。

主 Agent 职责：

```text
读取当前 feature 状态
选择第一个未完成 task
给 Sub Agent 下发最小任务
明确允许修改范围
明确禁止修改范围
明确验收标准
要求完成后停止
```

Sub Agent 职责：

```text
只执行当前 task
不主动扩展需求
不修改未授权文件
不新增依赖
不执行 git add
不执行 git commit
完成后输出结果并停止
```

Sub Agent 任务必须包含：

```text
当前 task 是什么
允许改哪些文件
禁止改哪些文件
需要运行哪些测试
完成标准是什么
停止条件是什么
```

错误示例：

```text
实现文档标题更新功能
```

正确示例：

```text
只执行 Task 1：为 PATCH /api/documents/{id}/title 添加失败测试。
只允许修改 src/test/java。
不允许修改 src/main/java。
不允许修改 pom.xml。
测试应因为功能尚未实现而失败。
完成后停止，输出修改文件和测试结果。
```

### 阶段 6：主 Agent 验收

目标：主 Agent 基于事实证据验收 Sub Agent 的结果，而不是只看 Sub Agent 的总结。

必须检查：

```text
git status
git diff
git diff --stat
测试结果
修改文件列表
是否越界修改
是否新增依赖
是否修改 pom.xml
是否降低测试断言
是否删除测试
是否绕过测试
是否改变 API 行为
是否只完成当前 task
```

验收结果只能是：

```text
通过
需要小修
拒绝，需要回滚或重做
```

如果通过：

```text
更新 task 状态
进入下一个 task
```

如果不通过：

```text
指出具体问题
要求 Sub Agent 小修
或回滚后重新执行
```

### 阶段 7：记录项目记忆

目标：把本次开发中产生的长期价值沉淀下来，避免下次重复犯错。

记录位置：

```text
docs/decisions/   # 关键决策
docs/lessons/     # AI 错误、工具坑、流程教训
AGENTS.md         # 稳定且必须默认遵守的 agent 规则
CLAUDE.md         # Claude Code 专用默认规则
WORKFLOW.md       # 工作流索引和选择规则
```

记录内容：

```text
为什么这样设计
为什么不采用其他方案
AI 出现了什么错误
哪些规则需要长期保留
哪些流程需要改进
哪些内容不应该塞进 agent 规则文件
```

注意：

```text
不是所有讨论都要写入记忆。
只有长期有效、会影响后续开发判断的内容才沉淀。
```

### 最终工作流摘要

```text
阶段 0：项目级上下文校准
  - product.md
  - tech.md
  - structure.md
  - AGENTS.md / CLAUDE.md
  - WORKFLOW.md
  - decisions / lessons

阶段 1：需求探索与反复讨论
  - AI grill me
  - 人和 AI 多轮讨论
  - 暴露歧义、边界、风险、非目标
  - 暂不写代码，暂不进入设计

阶段 2：需求定稿
  - 明确目标、非目标、边界、验收标准
  - 产出 requirements.md

阶段 3：设计评审
  - AI 提出 design.md
  - 人审查是否过度设计
  - 明确不新增哪些东西

阶段 4：任务拆分
  - 产出 tasks.md
  - 每个 task 必须小、可测试、可回滚
  - 每个 task 有完成标准

阶段 5：分 task 执行
  - 主 Agent 选择当前第一个未完成 task
  - Sub Agent 只执行这个 task
  - 完成后必须停止

阶段 6：主 Agent 验收
  - 查看 diff
  - 查看测试
  - 查看越界修改
  - 决定是否通过

阶段 7：记录项目记忆
  - 关键决策进 docs/decisions/
  - AI 错误进 docs/lessons/
  - 稳定规则同步到 AGENTS.md / CLAUDE.md
```

## 53. 主 Agent / Sub Agent 分工工作流

需要掌握：

1. 为什么复杂任务需要主 Agent / Sub Agent 分工
2. 主 Agent 负责规划、上下文校准、任务选择和验收
3. Sub Agent 只负责当前 task 的窄范围执行
4. 如何给 Sub Agent 下发最小任务
5. 如何限制 Sub Agent 的允许修改范围和禁止修改范围
6. 如何防止 Sub Agent 扩展需求、越界修改、跳过测试
7. 如何由主 Agent 基于 git diff、测试结果和修改范围做验收
8. 如何处理通过、小修、拒绝、回滚

## 54. 最终项目验收与流程固化

需要掌握：

1. 项目功能验收
2. 测试验收
3. 文档验收
4. 代码质量验收
5. AI 工作流验收
6. 工具链验收
7. 复盘整个学习路径
8. 形成个人 AI 辅助开发标准流程
9. 形成自己的 AGENTS.md / CLAUDE.md / Skills / Hooks / Review Checklist 模板
10. 明确后续哪些流程继续手动执行，哪些流程可以工具化

---

# 附录：推荐的项目规则优先级

当多个规则发生冲突时，建议按以下顺序处理：

```text
用户当前明确指令
    ↓
安全与权限边界
    ↓
项目长期规则：AGENTS.md / CLAUDE.md
    ↓
当前 Spec / Task 状态
    ↓
Skill 执行步骤
    ↓
Hook / MCP 工具结果
    ↓
AI 自己的默认判断
```

注意：

1. 安全与权限边界不能被普通任务指令覆盖。
2. 如果用户当前指令和项目长期规则冲突，AI 必须指出冲突并等待确认。
3. 如果 MCP 状态、Spec 文档、Git diff、测试结果不一致，不能直接继续实现，必须先对齐状态。
4. 如果 AI 不确定某条规则是否适用，应先说明不确定点，而不是擅自选择有利于继续写代码的解释。

---

# 附录：最小可用 AI 辅助开发闭环

即使不使用 MCP、Hooks、Subagents、Plugins，也应该至少做到：

```text
Git 基线
    ↓
明确任务
    ↓
AI 先定位修改点
    ↓
小步修改
    ↓
运行测试 / 手动验证
    ↓
查看 git diff
    ↓
AI Review
    ↓
人工确认
    ↓
commit
```

这条闭环是所有高级工具链的基础。
