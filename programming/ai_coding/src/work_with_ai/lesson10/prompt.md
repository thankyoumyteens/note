# 本课推荐 Prompt

```text
目标：
进入 TDD Red phase。
请为文档摘要功能 POST /api/documents/{id}/summary 编写失败测试。
当前阶段只允许写测试，不允许实现业务代码。

背景：
当前项目是 ai-doc-summary，已经完成：
1. POST /api/documents 文档保存功能。
2. GET /api/documents/{id} 文档查询功能。
3. GET /api/documents/{id}/metadata 文档元信息查询功能。
4. 当前项目已经具备 spec-workflow-mcp 相关工作流经验。
5. 当前开发流程要求：新行为优先先写测试，再写实现。

新增功能：
POST /api/documents/{id}/summary

功能意图：
根据已保存文档生成摘要。
当前阶段不接真实 AI API，不接 Spring AI。
后续实现阶段会使用 FakeAiSummaryClient 或本地 fake service 让测试通过。

当前只做 Red phase：
1. 新增或修改测试。
2. 不创建 SummaryController。
3. 不创建 SummaryService。
4. 不创建 FakeAiSummaryClient。
5. 不修改已有业务实现。
6. 不修改 pom.xml。
7. 不新增依赖。

测试要求：
请新增失败测试，至少覆盖：

1. 摘要生成成功
   - 先通过 POST /api/documents 创建文档。
   - 再调用 POST /api/documents/{documentId}/summary。
   - 期望状态码为 200 OK。
   - 响应包含 documentId。
   - 响应包含 summary。
   - summary 预期为固定 fake 规则，例如：
     "Summary: " + content

2. 文档不存在
   - 调用 POST /api/documents/999999/summary。
   - 期望返回 404 Not Found。

3. 回归测试
   - 现有 POST /api/documents 测试不受影响。
   - 现有 GET /api/documents/{id} 测试不受影响。
   - 现有 GET /api/documents/{id}/metadata 测试不受影响。
   - GET /api/health 不受影响。

允许修改：
1. 只允许新增或修改测试文件。
2. 可以新增 SummaryControllerTest 或 SummaryControllerTests。
3. 可以复用现有 MockMvc 测试结构。

禁止修改：
1. 不要修改 src/main/java 下的业务代码。
2. 不要新增 SummaryController。
3. 不要新增 SummaryService。
4. 不要新增 FakeAiSummaryClient。
5. 不要修改 InMemoryDocumentStore。
6. 不要修改 DocumentController。
7. 不要修改 pom.xml。
8. 不要新增依赖。
9. 不要接入真实 AI API。
10. 不要接入 Spring AI。
11. 不要加入数据库 / JPA。
12. 不要加入 Spring Security / 用户系统。
13. 不要运行 mvn spring-boot:run。
14. 不要执行 git add。
15. 不要执行 git commit。

执行要求：
1. 先检查当前测试结构。
2. 说明准备新增或修改哪个测试文件。
3. 只写测试。
4. 写完后运行 mvn test。
5. 预期 mvn test 应该失败。
6. 如果测试失败原因是 POST /api/documents/{id}/summary 尚未实现，这是正确结果。
7. 如果测试因为编译错误或测试本身写错失败，需要修正测试。
8. 不要为了让测试通过而写实现。

完成后输出：
1. 新增/修改了哪些测试文件。
2. 测试覆盖了哪些行为。
3. mvn test 是否失败。
4. 失败原因是否符合预期。
5. 是否修改了 src/main/java。
6. 是否修改了 pom.xml。
7. 是否新增依赖。
8. git status 摘要。
9. git diff --stat 摘要。
```
