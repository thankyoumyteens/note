# 第一步 Prompt：只实现模型和 DTO

先发这个给 Codex：

```text
目标：
开始第 7 课：小步实现文档保存功能。现在只执行第 1 小步：新增文档模型和 DTO。

背景：
第 6 课已经完成文档保存功能的实现计划。当前要实现 POST /api/documents，但必须小步进行。
本次只允许新增最小数据结构，不允许实现 Controller，不允许写业务逻辑，不允许写测试。

本次允许新增：
1. src/main/java/com/example/aidocsummary/document/Document.java
2. src/main/java/com/example/aidocsummary/document/DocumentRequest.java
3. src/main/java/com/example/aidocsummary/document/DocumentResponse.java

设计要求：
1. Document 包含 id、title、content。
2. DocumentRequest 包含 title、content。
3. DocumentResponse 只包含 documentId。
4. 使用普通 Java 类或 record 均可，但保持项目风格一致。
5. 不新增依赖。

限制：
1. 不要修改 pom.xml。
2. 不要修改 README.md。
3. 不要修改 AGENTS.md / CLAUDE.md。
4. 不要实现 DocumentController。
5. 不要实现 InMemoryDocumentStore。
6. 不要新增测试。
7. 不要接入数据库、AI API、Spring Security。
8. 不要让 DocumentResponse 返回 title 或 content。

完成后请输出：
1. 新增了哪些文件
2. 每个文件的用途
3. 是否修改了无关文件
4. 下一步建议
```

完成后你检查：

```bash
git diff --stat
git diff
```

理想情况下只新增 3 个文件。
