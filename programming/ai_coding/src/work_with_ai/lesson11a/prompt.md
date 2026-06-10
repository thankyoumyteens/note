# 本课推荐 Prompt

````text
目标：
进入 TDD Refactor phase。

请对当前 `POST /api/documents/{id}/summary` 的实现进行 Refactor 评估。

当前阶段不是继续加功能。
当前阶段不是为了“改而改”。
当前阶段目标是：在测试保护下，检查当前实现是否真实、简单、可维护；如有必要，只做小步、行为不变的重构。

请先评估是否需要重构。
不要一上来直接改代码。
不要修改构建配置。
不要新增依赖。
不要执行 git add / git commit。

背景：
当前项目是 `ai-doc-summary`，已经完成：

1. `GET /api/health`
2. `POST /api/documents`
3. `GET /api/documents/{id}`
4. `GET /api/documents/{id}/metadata`
5. `POST /api/documents/{id}/summary`
6. 已完成 TDD Red：先为 summary 行为编写失败测试。
7. 已完成 TDD Green：最小实现让 summary 测试通过。

当前阶段：
TDD Refactor phase：在测试保护下评估并小步重构。

请先读取：

1. `AGENTS.md`
2. `CLAUDE.md`
3. `WORKFLOW.md`
4. 当前 `src/main/java`
5. 当前 `src/test/java`
6. 当前 summary 相关实现
7. 当前 summary 相关测试
8. 当前 git status
9. 当前项目构建工具与构建配置文件

请先识别项目构建工具：

1. 如果存在 `pom.xml`，视为 Maven 项目。
2. 如果存在 `build.gradle` 或 `build.gradle.kts`，视为 Gradle 项目。
3. 如果同时存在 Maven 和 Gradle 配置，不要猜测，先报告冲突并等待确认。
4. 如果无法识别构建工具，停止并报告，不要假设使用 Maven 或 Gradle。
5. 优先使用项目自带 wrapper：

   * Maven 项目优先使用 `./mvnw test`，没有 wrapper 时再使用 `mvn test`。
   * Gradle 项目优先使用 `./gradlew test`，没有 wrapper 时再使用 `gradle test`。

构建配置文件包括但不限于：

1. `pom.xml`
2. `build.gradle`
3. `build.gradle.kts`
4. `settings.gradle`
5. `settings.gradle.kts`
6. `gradle.properties`
7. `mvnw`
8. `mvnw.cmd`
9. `gradlew`
10. `gradlew.bat`
11. 其他项目已有的构建脚本或依赖配置文件

第一步：
请先不要改代码。
先输出 Refactor 评估报告。

Refactor 评估报告必须包含：

1. 当前 summary 实现涉及哪些类和测试。
2. 当前实现是否符合功能意图，而不仅仅是测试通过。
3. 当前实现是否生成基于已保存文档 content 的 summary。
4. 当前实现是否正确处理文档不存在场景。
5. 当前实现是否保持已有文档 title / content / metadata 不被破坏。
6. 当前实现是否改变了已有接口行为。
7. 当前实现是否已经足够简单。
8. 是否存在 Controller 过重。
9. 是否存在 Service 责任不清。
10. 是否存在重复代码。
11. 是否存在命名不清。
12. 是否存在不必要抽象。
13. 是否存在过度设计。
14. 是否存在项目边界风险。
15. 是否需要重构。
16. 如果需要，只列出最小重构计划。

必须额外进行 Implementation Integrity Review：

1. 当前实现是否只是为了让测试通过而写的 fake implementation。
2. 是否存在 hardcoded exception。
3. 是否存在 hardcoded return。
4. 是否存在 empty implementation。
5. 是否存在 ignored input。
6. 是否存在只实现错误路径。
7. 是否存在只实现成功路径。
8. 是否存在 response-only fake that ignores stored document content。
9. 是否存在绕过存储层或绕过已有业务流程。
10. 是否存在测试覆盖不足导致的假绿。
11. 当前测试是否足以证明实现符合功能意图。
12. 如果测试不足，是否应该回到 Red phase 补测试。
13. 如果实现不真实，是否应该回到 Green phase 修正，而不是进入 Refactor。

如果发现当前实现只是 test-passing fake：
不要说“不需要重构”。
不要进入普通重构。
请停止并输出：

1. 哪段实现是 fake 或不完整实现。
2. 它违反了哪个功能意图。
3. 哪些测试缺失或断言太弱。
4. 应该回到 Red phase 补哪些测试。
5. 或应该回到 Green phase 修正哪些实现。
6. 当前不应进入 Refactor 的原因。

只有在当前实现行为真实、测试通过、功能意图满足的前提下，才允许判断是否需要普通重构。

重构边界：

1. 只允许重构已有 summary 相关实现。
2. 不新增业务功能。
3. 不修改 API 行为。
4. 不修改响应 JSON 结构。
5. 不降低测试断言。
6. 不删除已有 summary 测试。
7. 不删除成功路径测试。
8. 不删除 404 测试。
9. 不删除防 fake implementation 的测试。
10. 不修改任何构建配置文件。
11. 不新增依赖。
12. 不接真实 AI API。
13. 不接 Spring AI。
14. 不接数据库 / JPA。
15. 不加 Spring Security / 用户系统。
16. 不实现缓存 / 历史 / 异步任务。
17. 不运行长期占用进程的启动命令，例如 spring boot run、bootRun、run、start、dev server。
18. 不执行 git add。
19. 不执行 git add -N。
20. 不执行 git commit。

如果评估认为不需要重构：
请明确说明原因，并运行对应构建工具的测试命令：

* Maven：优先 `./mvnw test`，没有 wrapper 时用 `mvn test`。
* Gradle：优先 `./gradlew test`，没有 wrapper 时用 `gradle test`。

然后输出测试结果、git 状态、untracked files 检查和结论。

如果评估认为需要重构：
请按小步执行：

1. 每次只做一个重构动作。
2. 每个重构动作必须行为不变。
3. 每步说明改了哪些文件。
4. 每步后运行相关测试；必要时运行完整测试。
5. 每步后输出 git status、git diff --stat 和 untracked files 列表。
6. 如果测试失败，先解释原因，不要继续扩大修改。
7. 如果发现测试不足或实现不真实，停止并建议回到 Red / Green，不要继续 Refactor。

测试要求：

1. 运行对应构建工具的测试命令：

   * Maven：优先 `./mvnw test`，没有 wrapper 时用 `mvn test`。
   * Gradle：优先 `./gradlew test`，没有 wrapper 时用 `gradle test`。
2. summary 相关测试必须通过。
3. 既有接口测试必须通过：

   * `POST /api/documents`
   * `GET /api/documents/{id}`
   * `GET /api/documents/{id}/metadata`
   * `GET /api/health`
4. 不允许通过修改测试来制造通过。
5. 不允许降低断言强度。
6. 不允许删除测试。

完成后输出：

1. 识别到的构建工具。
2. 使用的测试命令。
3. 是否进行了重构。
4. 如果没有重构，为什么不需要。
5. 如果没有进入 Refactor，而是发现 fake implementation，说明为什么应该回到 Red / Green。
6. 如果进行了重构，修改了哪些文件。
7. 每个修改是否行为不变。
8. 是否修改了 API 行为。
9. 是否修改了响应 JSON 结构。
10. 是否修改了测试断言。
11. 是否删除了测试。
12. 是否修改了构建配置文件。
13. 是否新增依赖。
14. 是否引入真实 AI API / Spring AI / 数据库 / JPA / Security / 用户系统。
15. 测试结果。
16. 是否有任何越界修改。
17. 是否建议进入下一阶段，但当前阶段不要执行下一阶段任务。
18. 是否执行 git add / git add -N / git commit。

Git 检查必须包含：

1. `git status --short` 摘要。
2. `git diff --stat` 摘要，用于显示 tracked 文件改动。
3. untracked files 列表，用于显示新创建但尚未被 Git 追踪的文件。
4. 如果存在 untracked files，必须逐个说明：

   * 文件路径
   * 文件用途
   * 为什么需要新建
   * 是否属于本次任务允许范围。
5. 不允许因为 `git diff --stat` 无输出就声称“没有修改”。
6. 如果 `git status --short` 出现 `??`，必须明确说明存在新文件。
7. 不要执行 `git add`。
8. 不要执行 `git add -N`。
9. 不要执行 `git commit`。

建议使用的 Git 检查命令：

```bash
git status --short
git diff --stat
git ls-files --others --exclude-standard
```
````
