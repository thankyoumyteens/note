# 第一步：让 Codex 先读取 spec，不改代码

先发这个 prompt：

```text
目标：
开始第 9 课：Spec 驱动实现文档查询功能。请先读取 spec 并检查，不要修改代码。

背景：
当前项目是 ai-doc-summary，已经完成：
1. POST /api/documents 文档保存功能
2. specs/document-query/ 轻量 spec
3. 第 8 课已完成，但尚未实现 GET /api/documents/{id}

输入：
请读取以下文件：
1. AGENTS.md
2. CLAUDE.md
3. specs/document-query/requirements.md
4. specs/document-query/design.md
5. specs/document-query/tasks.md
6. specs/document-query/test.md
7. 当前 document 包相关源码和测试
8. 当前 git status

输出：
请先不要修改代码。
请输出：
1. 当前任务目标
2. Scope
3. Non-goals
4. Acceptance Criteria
5. 当前 tasks.md 任务列表
6. 预计需要修改哪些文件
7. 明确不应该修改哪些文件
8. 是否发现 spec 与当前代码冲突
9. 如果没有严重冲突，请给出第 9 课实现顺序

限制：
1. 不要修改 Java 源码。
2. 不要修改 pom.xml。
3. 不要新增依赖。
4. 不要更新 tasks.md。
5. 不要实现 GET /api/documents/{id}。
6. 本步只做 spec 读取和冲突检查。
```

这一步的目的不是实现，而是确认 Codex 真的按 spec 理解任务。

---

## 你要检查 Codex 的读取结果

重点看这些：

```text
1. 它是否明确目标是 GET /api/documents/{id}
2. 它是否知道成功返回 documentId、title、content
3. 它是否知道不存在返回 404
4. 它是否知道继续使用内存存储
5. 它是否知道不能改 POST /api/documents 响应格式
6. 它是否知道不能改 pom.xml
7. 它是否知道不能新增依赖
8. 它是否发现 spec 和当前代码是否冲突
```

如果它说要加数据库、JPA、H2、Repository、Bean Validation、新依赖，就说明它偏离了 spec。

纠正 prompt：

```text
当前计划偏离 specs/document-query/ 的 Non-goals。
请重新读取 requirements.md 和 design.md。
本功能不接数据库、不新增依赖、不使用 JPA、不改变 POST /api/documents 响应格式。
请重新输出实现顺序，不要修改代码。
```
