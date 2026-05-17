# 第二步：按 tasks.md 小步实现

如果第一步检查通过，再让 Codex 按任务实现。

推荐 prompt：

```text
目标：
继续第 9 课：按 specs/document-query/tasks.md 逐项实现 GET /api/documents/{id}。

前提：
你已经读取并确认 specs/document-query/ 下的 requirements.md、design.md、tasks.md、test.md 没有严重冲突。

执行要求：
1. 按 tasks.md 逐项实现。
2. 每次只完成一个小任务。
3. 每完成一项，更新 tasks.md 的 checkbox。
4. 不要实现 Non-goals 中排除的内容。
5. 不要修改 pom.xml。
6. 不要新增依赖。
7. 不要接入数据库。
8. 不要接入 AI API。
9. 不要加入用户系统或 Spring Security。
10. 不要实现文档列表查询。
11. 不要实现摘要功能。
12. 不要改变 POST /api/documents 的成功响应格式。
13. 如果需要修改 Java 代码，只修改 spec 中涉及的 document 包相关文件和对应测试。
14. 如果发现 spec 与代码冲突，先停止并报告，不要猜。

实现目标：
1. InMemoryDocumentStore 支持按 id 查询文档。
2. DocumentController 新增 GET /api/documents/{id}。
3. 查询成功返回 200 OK。
4. 查询成功响应包含 documentId、title、content。
5. 查询不存在返回 404 Not Found。
6. 错误响应保持简单，例如 {"error":"document not found"}。
7. 添加或更新测试，覆盖成功查询和不存在查询。
8. 确保现有 POST /api/documents 测试继续通过。
9. 确保健康检查测试继续通过。

完成后请输出：
1. 完成了 tasks.md 中哪些任务
2. 修改了哪些文件
3. 是否更新了 tasks.md
4. 是否更新了 test.md
5. 是否修改了不该修改的文件
6. 下一步应该运行的命令
```
