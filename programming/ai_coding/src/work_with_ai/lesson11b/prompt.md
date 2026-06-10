# 本课推荐 Prompt

````text
目标：
为当前项目创建 / 强化通用 TDD Skill 工作流。

任务目标：
把 TDD 的 Red / Green / Refactor 三个阶段固化成可复用 Skill。

这次不是开发业务功能。
不要修改业务代码。
不要修改测试代码。
不要修改构建配置。
不要新增依赖。
不要执行 git add / git add -N / git commit。

背景：
当前项目需要建立一套通用 TDD 工作流，用于后续任何非平凡功能开发。

核心目标：

1. Red 阶段：生成能约束真实业务行为的失败测试，防止测试不完整。
2. Green 阶段：用符合功能意图的最小有效实现让测试通过，防止 fake implementation。
3. Refactor 阶段：在测试保护下评估并小步重构，防止把“假绿”误判为不需要重构。
4. 所有阶段都要兼容不同构建工具，例如 Maven、Gradle、npm、pnpm、yarn、pytest、go test、cargo test 等。
5. 所有阶段都要正确检查 Git tracked changes 和 untracked files。

请先读取：

1. 项目规则文件，例如：

   * AGENTS.md
   * CLAUDE.md
   * README.md
   * CONTRIBUTING.md
   * WORKFLOW.md
   * 其他项目已有的 agent / workflow / coding rules
2. 现有 `skills/` 目录，如果存在。
3. 当前测试目录。
4. 当前源代码目录结构。
5. 当前 git status。
6. 当前项目构建工具与测试命令。

请先识别项目类型和构建工具：

1. 如果存在 `pom.xml`，可能是 Maven 项目。
2. 如果存在 `build.gradle` 或 `build.gradle.kts`，可能是 Gradle 项目。
3. 如果存在 `package.json`，可能是 Node / TypeScript / JavaScript 项目。
4. 如果存在 `pyproject.toml`、`requirements.txt`、`setup.py`，可能是 Python 项目。
5. 如果存在 `go.mod`，可能是 Go 项目。
6. 如果存在 `Cargo.toml`，可能是 Rust 项目。
7. 如果存在多个构建系统，不要猜测，先报告冲突并等待确认。
8. 如果无法识别构建工具或测试命令，停止并报告，不要自行假设。
9. 优先使用项目自带 wrapper 或已有脚本：

   * Maven：优先 `./mvnw test`，没有 wrapper 时再使用 `mvn test`
   * Gradle：优先 `./gradlew test`，没有 wrapper 时再使用 `gradle test`
   * Node：优先使用 `package.json` 中已有 test script，例如 `npm test`、`pnpm test`、`yarn test`
   * Python：根据项目配置使用已有命令，例如 `pytest`、`python -m pytest`、`tox`
   * Go：通常使用 `go test ./...`
   * Rust：通常使用 `cargo test`
10. 不要新增测试框架或依赖，除非用户明确确认。

构建配置文件包括但不限于：

1. `pom.xml`
2. `build.gradle`
3. `build.gradle.kts`
4. `settings.gradle`
5. `settings.gradle.kts`
6. `gradle.properties`
7. `package.json`
8. `package-lock.json`
9. `pnpm-lock.yaml`
10. `yarn.lock`
11. `pyproject.toml`
12. `requirements.txt`
13. `setup.py`
14. `tox.ini`
15. `go.mod`
16. `go.sum`
17. `Cargo.toml`
18. `Cargo.lock`
19. wrapper scripts
20. 其他项目已有的构建、依赖或测试配置文件

第一步：
请先不要改文件。
先输出 TDD Skill 设计计划，说明：

1. 准备创建或修改哪些 Skill。
2. 每个 Skill 的用途。
3. 每个 Skill 的输入。
4. 每个 Skill 的输出。
5. 每个 Skill 的禁止事项。
6. 每个 Skill 的完成标准。
7. 如何让 `tdd-red` 防止测试不完整。
8. 如何让 `tdd-green` 防止 fake implementation。
9. 如何让 `tdd-refactor` 防止把 fake implementation 误判为“不需要重构”。
10. 如何识别项目构建工具和测试命令。
11. 如何检查 tracked changes 和 untracked files。
12. 是否需要小幅更新项目 workflow / agent 规则文件。
13. 本次准备修改哪些文件。
14. 哪些文件明确不修改。

确认计划后，再创建或修改文件。

允许新增或修改：

1. `skills/tdd-red/SKILL.md`
2. `skills/tdd-green/SKILL.md`
3. `skills/tdd-refactor/SKILL.md`

可选新增：

1. `skills/tdd-cycle/SKILL.md`

允许小幅修改：

1. 项目 workflow 索引文件，例如 `WORKFLOW.md`
2. 项目 agent 规则文件，例如 `AGENTS.md`、`CLAUDE.md`
3. 其他项目已有的规则入口文件

修改要求：

1. workflow 索引文件只写 TDD Skill 索引和选择规则，不写长篇执行细节。
2. agent 规则文件只写何时必须使用 TDD Skill 的默认规则。
3. Skill 内容必须兼容不同 AI coding tools，不写成只适合某一个工具。
4. Skill 内容必须兼容不同构建工具，不写死 Maven、Gradle 或任何单一命令。
5. Skill 内容必须要求先识别构建工具，再选择测试命令。
6. Skill 内容必须要求 Git 检查包含：

   * `git status --short`
   * tracked changes summary
   * untracked files list

禁止修改：

1. 不修改业务源代码。
2. 不修改测试代码。
3. 不修改任何构建配置文件。
4. 不新增依赖。
5. 不实现新接口或新功能。
6. 不修改已有功能行为。
7. 不接入新的外部服务。
8. 不引入数据库、鉴权、缓存、队列、前端、部署等额外架构能力。
9. 不运行长期占用进程的启动命令，例如 dev server、application server、watch mode、run server、start server。
10. 不执行 `git add`。
11. 不执行 `git add -N`。
12. 不执行 `git commit`。

每个 Skill 必须包含：

1. YAML frontmatter：
   - name
   - description
2. Purpose
3. When to use
4. Inputs
5. Steps
6. Output format
7. Hard rules
8. Completion checklist
9. Common mistakes to avoid

`tdd-red` 必须强调：

1. Red 阶段不是随便写一个失败测试。
2. Red 阶段必须写能约束真实业务行为的失败测试。
3. Red 阶段必须先输出 Test Coverage Plan。
4. 对于非平凡功能，测试计划必须覆盖：

   * Feature intent
   * Success path
   * Error path
   * State change / persistence check，如果功能会改变状态
   * Non-target field check，如果功能只应修改部分状态
   * Response contract，如果存在 API、CLI、事件、消息、返回对象或 UI contract
   * Input-output relation
   * Boundary cases，按需求选择
   * Regression check，按影响范围选择
   * Fake implementation risks
   * Red expectation
5. 不允许只写错误路径测试来驱动一个需要成功行为的功能。
6. 不允许只写成功路径测试而忽略明确要求的错误路径。
7. 不允许只验证 status code、exit code、异常类型或字段存在。
8. 不允许只验证是否抛异常，除非当前需求本身就是错误处理行为。
9. 不允许写能被 hardcoded return、hardcoded exception、empty implementation、ignored input 轻易骗过的测试。
10. 如果功能会改变状态，必须验证状态真的改变。
11. 如果功能只应修改部分状态，必须验证非目标字段或非目标资源不变。
12. 如果测试不足以约束真实行为，必须停止并指出缺失测试，不允许进入 Green。
13. 只允许修改测试文件。
14. 不允许修改生产代码。
15. 不允许修改构建配置。
16. 测试失败原因必须是功能尚未实现或行为尚未满足，不能是测试写错、编译错误、构建命令错误或环境问题。

`tdd-green` 必须强调：

1. Green 阶段不是单纯让测试通过。
2. Green 阶段必须用符合功能意图的最小有效实现让测试通过。
3. 实现前必须读取失败测试和 feature intent。
4. 实现前必须检查 Red 测试是否足以防止 fake implementation。
5. 如果测试只覆盖错误路径、只验证异常、只验证 status code、只验证字段存在、没有成功路径、没有输入输出关系，必须停止并建议回到 Red phase 补测试。
6. 不允许用 hardcoded exception 让测试通过。
7. 不允许用 hardcoded return 让测试通过。
8. 不允许 empty implementation。
9. 不允许 ignored input。
10. 不允许只实现错误路径。
11. 不允许只实现成功路径而破坏错误路径。
12. 不允许 response-only fake，尤其是需要状态变化时只改响应不改状态。
13. 不允许修改测试来适配实现。
14. 不允许降低测试断言。
15. 不允许删除测试。
16. 不扩大功能范围。
17. 不修改构建配置。
18. 不新增依赖。
19. 测试命令必须根据实际项目识别结果选择。

`tdd-refactor` 必须强调：

1. 测试通过后才允许进入 Refactor。
2. Refactor 前必须先做 Refactor 评估。
3. Refactor 前必须先做 Implementation Integrity Review。
4. 不能只因为“测试通过 + 代码简单”就判断不需要重构。
5. 必须检查当前实现是否符合功能意图，而不仅仅是测试通过。
6. 必须检查是否存在：

   * hardcoded exception
   * hardcoded return
   * empty implementation
   * ignored input
   * only-error-path implementation
   * only-success-path implementation
   * response-only fake
   * state-not-updated fake
   * bypassed business flow
   * 测试覆盖不足导致的假绿
7. 如果发现当前实现是 test-passing fake，不允许说“不需要重构”。
8. 如果实现不真实，必须建议回到 Red / Green 修正，而不是继续 Refactor。
9. 只有实现行为真实、测试通过、功能意图满足时，才允许普通重构评估。
10. 不为了改而改。
11. 不新增业务功能。
12. 不修改外部行为、API contract、CLI contract、事件 contract、消息 contract 或返回结构。
13. 不降低测试断言。
14. 不删除测试。
15. 每步重构后运行相关测试或完整测试。
16. 不修改构建配置。
17. 不新增依赖。

`tdd-cycle` 如果创建，必须强调：

1. Red → Green → Refactor 顺序不可跳过。
2. Red 不完整时不能进入 Green。
3. Green 出现 fake implementation 时不能进入 Refactor。
4. Refactor 发现假绿时必须退回 Red / Green。
5. 每个 phase 完成后必须输出边界检查和 Git 检查。
6. 每个 phase 结束后等待用户确认，不自动进入下一阶段。

Git 检查规则必须写入每个 Skill：

1. 不允许只依赖 `git diff --stat` 判断是否有修改。
2. `git diff --stat` 只显示 tracked files 的改动。
3. 新创建但未被 Git 追踪的文件必须通过 untracked files list 检查。
4. 每个 Skill 输出时必须包含：

   * `git status --short`
   * tracked changes summary
   * untracked files list
5. 如果 `git status --short` 出现 `??`，必须明确说明存在新文件。
6. 如果存在 untracked files，必须逐个说明：

   * 文件路径
   * 文件用途
   * 为什么需要新建
   * 是否属于本次任务允许范围
7. 不允许因为 tracked diff 无输出就声称“没有修改”。
8. 不执行 `git add`。
9. 不执行 `git add -N`。
10. 不执行 `git commit`。

建议 Git 检查命令：

```bash
git status --short
git diff --stat
git ls-files --others --exclude-standard
```

完成后输出：

1. 识别到的项目类型。
2. 识别到的构建工具。
3. 推荐测试命令。
4. 创建/修改了哪些文件。
5. 每个 Skill 的主要内容摘要。
6. `tdd-red` 新增了哪些测试完整性规则。
7. `tdd-green` 新增了哪些防 fake implementation 规则。
8. `tdd-refactor` 新增了哪些 implementation integrity review 规则。
9. `tdd-cycle` 是否创建。
10. workflow 索引文件是否只保留索引和选择规则。
11. 是否修改 agent 规则文件。
12. 是否修改业务源代码。
13. 是否修改测试代码。
14. 是否修改任何构建配置文件。
15. 是否新增依赖。
16. 是否运行测试；如果运行，使用了哪个命令。
17. 是否执行 git add / git add -N / git commit。
18. `git status --short` 摘要。
19. tracked changes 摘要。
20. untracked files 列表。
21. 是否可以进入后续 feature workflow 实践。
````
