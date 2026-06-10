# 本课推荐 Prompt

````text
目标：
进入 TDD Red phase。
请为文档摘要功能 `POST /api/documents/{id}/summary` 编写失败测试。

当前阶段只允许写测试。
不允许实现业务代码。
不允许修改构建配置。
不允许新增依赖。
不允许执行 git add / git commit。

背景：
当前项目是 `ai-doc-summary`，已经完成：

1. `POST /api/documents` 文档保存功能。
2. `GET /api/documents/{id}` 文档查询功能。
3. `GET /api/documents/{id}/metadata` 文档元信息查询功能。
4. 当前项目已经具备 spec-workflow-mcp 相关工作流经验。
5. 当前开发流程要求：新行为先写测试，再写实现。

新增功能：
`POST /api/documents/{id}/summary`

功能意图：
根据已保存文档生成摘要。

当前阶段不接真实 AI API。
当前阶段不接 Spring AI。
后续 Green phase 会使用 FakeAiSummaryClient 或本地 fake service 让测试通过。

当前只做 Red phase：

1. 新增或修改测试。
2. 不创建 SummaryController。
3. 不创建 SummaryService。
4. 不创建 FakeAiSummaryClient。
5. 不修改已有业务实现。
6. 不修改任何构建配置文件。
7. 不新增依赖。

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
先检查当前测试结构和构建工具。
不要立即写测试。

请先输出 Test Coverage Plan，必须包含：

1. Feature intent

   * 文档摘要功能真正要实现什么。
   * 本次只要求 fake summary。
   * 本次不引入真实 AI、Spring AI、数据库、用户系统、权限系统或异步任务。

2. Success path

   * 已存在文档时，可以生成摘要。
   * 必须先通过已有 `POST /api/documents` 创建文档。
   * 再调用 `POST /api/documents/{documentId}/summary`。
   * 期望返回 `200 OK`。
   * 响应必须包含 `documentId`。
   * 响应必须包含 `summary`。
   * `summary` 必须和原始 `content` 存在明确输入输出关系，例如：
     `Summary: ` + content。
   * 不允许只验证 `summary` 字段存在。
   * 不允许只验证 `summary` 非空。

3. Error path

   * 文档不存在时调用 `POST /api/documents/{id}/summary`。
   * 期望返回 `404 Not Found`。
   * 该测试不能成为唯一测试。
   * 必须同时存在成功路径测试，防止 Green 阶段只实现错误路径。

4. State / persistence check

   * 当前摘要功能如果只生成响应、不保存摘要历史，则必须明确：
     `summary generation is response-only in current scope`。
   * 本次不要求摘要持久化。
   * 但必须验证生成摘要不会破坏原文档。
   * 调用 summary 接口后，应通过 `GET /api/documents/{id}` 再次查询原文档。

5. Non-target field check

   * 生成摘要不应该修改文档标题或正文。
   * 如果当前文档模型包含 `title` 和 `content`，测试应验证：

     * `content` 仍保持原值。
     * `title` 仍保持原值，如果现有查询响应包含 title。
   * 如果现有响应不包含某字段，请在计划中说明原因。

6. Response contract

   * 成功响应必须包含：

     * `documentId`
     * `summary`
   * 成功响应不应该包含不属于当前 summary response contract 的字段。
   * 如果当前项目尚未定义 forbidden fields，必须说明暂不检查的原因。

7. Input-output relation

   * summary 必须来自创建文档时提交的 `content`。
   * 测试必须使用一个不容易被硬编码猜中的 content。
   * 不允许只断言 summary 非空。
   * 不允许只断言 summary 字段存在。
   * 不允许使用能被固定字符串轻易骗过的断言。

8. Boundary / validation cases

   * 当前功能主要输入是 `documentId`。
   * 必须覆盖 documentId 不存在。
   * 如果路径变量类型或框架会自然处理非法 ID，可以说明是否不在本次测试范围。
   * 不要机械添加和当前需求无关的边界测试。

9. Regression check

   * 确认新增 summary 测试不会破坏已有功能：

     * `POST /api/documents`
     * `GET /api/documents/{id}`
     * `GET /api/documents/{id}/metadata`
     * `GET /api/health`
   * 如果已有测试已经覆盖这些行为，可以复用现有测试，不必重复写相同测试。
   * 必须说明依赖哪些既有测试作为回归保护。

10. Fake implementation risks

    * 说明本组测试如何防止以下伪实现：

      * hardcoded exception
      * hardcoded return
      * empty implementation
      * ignored input
      * only-error-path implementation
      * only-success-path implementation
      * response-only fake that ignores document content
      * summary not based on stored document content
      * implementation that corrupts existing document data

11. Red expectation

    * 预期测试失败原因应该是：

      * `POST /api/documents/{id}/summary` 尚未实现，或
      * 对应 controller / route / handler 尚不存在，或
      * summary 行为尚未实现。
    * 如果失败原因是编译错误、测试写错、构建工具命令错误、断言不合理或环境问题，必须修正测试。
    * 不允许为了让测试通过而写生产代码。

测试要求：
请新增失败测试，至少覆盖：

1. 摘要生成成功

   * 先通过 `POST /api/documents` 创建文档。
   * 使用一个具体且不容易被硬编码猜中的 `content`。
   * 再调用 `POST /api/documents/{documentId}/summary`。
   * 期望状态码为 `200 OK`。
   * 响应包含 `documentId`。
   * 响应包含 `summary`。
   * `summary` 必须符合 fake 规则，例如：
     `Summary: ` + content。
   * 必须验证 summary 和输入 content 的关系。
   * 不允许只验证 summary 非空。

2. 文档不存在

   * 调用 `POST /api/documents/999999/summary`。
   * 期望返回 `404 Not Found`。
   * 该测试不能成为唯一测试，必须同时存在成功路径测试。

3. 原文档不被破坏

   * 先创建文档。
   * 调用 summary 接口。
   * 再通过 `GET /api/documents/{documentId}` 查询文档。
   * 验证原 `content` 仍保持不变。
   * 如果响应包含 title，也验证 title 保持不变。

4. 回归保护

   * 现有 `POST /api/documents` 测试不受影响。
   * 现有 `GET /api/documents/{id}` 测试不受影响。
   * 现有 `GET /api/documents/{id}/metadata` 测试不受影响。
   * `GET /api/health` 不受影响。
   * 如果已有测试已经覆盖这些行为，说明复用哪些现有测试即可。

允许修改：

1. 只允许新增或修改测试文件。
2. 可以新增 `SummaryControllerTest`、`SummaryControllerTests` 或符合当前项目命名风格的测试类。
3. 可以复用现有 MockMvc 测试结构。
4. 可以使用当前项目已有测试依赖。

禁止修改：

1. 不要修改 `src/main/java` 下的业务代码。
2. 不要新增 SummaryController。
3. 不要新增 SummaryService。
4. 不要新增 FakeAiSummaryClient。
5. 不要修改 InMemoryDocumentStore。
6. 不要修改 DocumentController。
7. 不要修改任何构建配置文件。
8. 不要新增依赖。
9. 不要接入真实 AI API。
10. 不要接入 Spring AI。
11. 不要加入数据库 / JPA。
12. 不要加入 Spring Security / 用户系统。
13. 不要运行长期占用进程的启动命令，例如 spring boot run、bootRun、run、start、dev server。
14. 不要执行 git add。
15. 不要执行 git add -N。
16. 不要执行 git commit。

执行要求：

1. 先检查当前测试结构。
2. 先识别构建工具。
3. 说明准备新增或修改哪个测试文件。
4. 先输出 Test Coverage Plan。
5. 再只写测试。
6. 写完后运行对应构建工具的测试命令：

   * Maven：优先 `./mvnw test`，没有 wrapper 时用 `mvn test`。
   * Gradle：优先 `./gradlew test`，没有 wrapper 时用 `gradle test`。
7. 预期测试应该失败。
8. 如果失败原因是 `POST /api/documents/{id}/summary` 尚未实现，这是正确结果。
9. 如果测试因为编译错误、测试本身写错、构建工具命令错误或断言不合理失败，需要修正测试。
10. 不要为了让测试通过而写实现。

完成后输出：

1. 识别到的构建工具。
2. 使用的测试命令。
3. 新增/修改了哪些测试文件。
4. Test Coverage Plan 摘要。
5. 测试覆盖了哪些行为。
6. 这些测试如何防止 fake implementation。
7. 测试是否失败。
8. 失败原因是否符合 Red phase 预期。
9. 是否修改了 `src/main/java`。
10. 是否修改了测试以外的文件。
11. 是否修改了构建配置文件。
12. 是否新增依赖。
13. 是否执行 git add / git add -N / git commit。

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
