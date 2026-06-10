# 本课推荐 Prompt

````text
目标：
进入 TDD Green phase。

请基于当前已经写好的 summary 失败测试，实现 `POST /api/documents/{id}/summary`。

当前目标不是“随便让测试通过”。
当前目标是：用符合功能意图的最小有效实现，让现有失败测试通过。

当前阶段允许写最小业务实现。
不允许做额外重构。
不允许扩展功能。
不允许修改构建配置。
不允许新增依赖。
不允许执行 git add / git commit。

背景：
当前项目是 `ai-doc-summary`，已经完成：

1. `POST /api/documents` 文档保存功能。
2. `GET /api/documents/{id}` 文档查询功能。
3. `GET /api/documents/{id}/metadata` 文档元信息查询功能。
4. 已经为 `POST /api/documents/{id}/summary` 写好失败测试。
5. 当前阶段允许写最小实现，但不做额外重构和功能扩展。

请先读取：

1. `AGENTS.md`
2. `CLAUDE.md`
3. `WORKFLOW.md`
4. 当前 `src/main/java`
5. 当前 `src/test/java`
6. 当前 summary 相关失败测试
7. 当前 git status
8. 当前项目构建工具与构建配置文件

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
先输出 Green Implementation Plan。

Green Implementation Plan 必须包含：

1. 当前失败测试覆盖了哪些行为。
2. 失败原因是否是 summary 接口尚未实现或行为尚未满足。
3. 当前测试是否覆盖成功路径。
4. 当前测试是否覆盖错误路径。
5. 当前测试是否验证 summary 和原始 content 的输入输出关系。
6. 当前测试是否验证原文档不会被 summary 生成破坏。
7. 当前测试是否足以防止以下伪实现：

   * hardcoded exception
   * hardcoded return
   * empty implementation
   * ignored input
   * only-error-path implementation
   * only-success-path implementation
   * response-only fake that ignores stored document content
   * implementation that corrupts existing document data
8. 如果测试不足以防止伪实现，必须停止并报告缺失测试。
9. 为了让测试通过，最小需要修改哪些文件。
10. 是否需要新增 `SummaryController` / `SummaryService` / `FakeAiSummaryClient` / `SummaryResponse`。
11. 是否需要修改 `InMemoryDocumentStore`。
12. 是否存在过度设计风险。
13. 是否存在实现越界风险。

如果当前测试只覆盖错误路径、只验证异常、只验证 HTTP status、只验证 summary 存在、没有验证输入输出关系，或者没有成功路径测试：
请停止。
不要写生产代码。
请指出缺失测试，并建议回到 Red phase 补测试。

等我确认后，再进入实现。

实现要求：

1. 实现 `POST /api/documents/{id}/summary`。
2. 文档存在时返回 `200 OK`。
3. 响应包含 `documentId` 和 `summary`。
4. `summary` 必须符合当前测试中的固定 fake 规则，例如：
   `Summary: ` + content。
5. `summary` 必须来自已保存文档的 content，不允许忽略输入。
6. 文档不存在时返回 `404 Not Found`。
7. 使用 `FakeAiSummaryClient` 或本地 fake service。
8. 只使用当前项目已有的内存存储。
9. 保持实现最小。
10. 不顺手重构无关代码。
11. 不改变已有接口行为：

    * `POST /api/documents`
    * `GET /api/documents/{id}`
    * `GET /api/documents/{id}/metadata`
    * `GET /api/health`
12. 不破坏已保存文档的 title / content / metadata。

Green phase 禁止伪实现：

1. 不允许用硬编码异常让测试通过。
2. 不允许只实现错误路径。
3. 不允许只实现成功路径而破坏错误路径。
4. 不允许返回固定 summary 且忽略文档 content。
5. 不允许直接返回请求外固定数据。
6. 不允许空实现。
7. 不允许绕过存储层。
8. 不允许只构造响应而不读取已保存文档。
9. 不允许修改测试来适配实现。
10. 不允许降低测试断言强度。
11. 不允许删除失败测试。
12. 不允许为了测试通过而改变功能意图。

禁止事项：

1. 不要修改任何构建配置文件。
2. 不要新增 Java 依赖。
3. 不要接真实 AI API。
4. 不要接 Spring AI。
5. 不要加入数据库 / JPA。
6. 不要加入 Spring Security / 用户系统。
7. 不要实现摘要缓存。
8. 不要实现摘要历史。
9. 不要实现异步摘要任务。
10. 不要实现文件上传。
11. 不要运行长期占用进程的启动命令，例如 spring boot run、bootRun、run、start、dev server。
12. 不要执行 git add。
13. 不要执行 git add -N。
14. 不要执行 git commit。

测试要求：

1. 运行对应构建工具的测试命令：

   * Maven：优先 `./mvnw test`，没有 wrapper 时用 `mvn test`。
   * Gradle：优先 `./gradlew test`，没有 wrapper 时用 `gradle test`。
2. summary 相关测试应通过。
3. 已有 `POST /api/documents` 测试应通过。
4. 已有 `GET /api/documents/{id}` 测试应通过。
5. 已有 `GET /api/documents/{id}/metadata` 测试应通过。
6. `GET /api/health` 测试应通过。
7. 如果测试失败，不要盲目改测试；先判断是实现问题、测试问题、构建工具问题还是环境问题。

完成后输出：

1. 识别到的构建工具。
2. 使用的测试命令。
3. 新增/修改了哪些文件。
4. 实现了哪些最小代码。
5. 这些实现如何满足功能意图，而不是仅仅骗过测试。
6. 这些实现如何避免 fake implementation。
7. 测试结果。
8. summary 相关测试是否通过。
9. 既有回归测试是否通过。
10. 是否修改了 `src/test/java`。
11. 是否修改了测试断言。
12. 是否修改了测试以外的无关文件。
13. 是否修改了构建配置文件。
14. 是否新增依赖。
15. 是否接入真实 AI API / Spring AI。
16. 是否引入数据库 / JPA / Security / 用户系统。
17. 是否有任何越界修改。
18. 是否还有需要进入 Refactor phase 的问题，但当前阶段不要执行重构。
19. 是否执行 git add / git add -N / git commit。

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
