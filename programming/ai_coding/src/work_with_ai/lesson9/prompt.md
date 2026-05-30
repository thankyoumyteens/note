# 本课推荐 Prompt

```text
目标：
按照 specs/document-query/ 中的轻量 Spec，实现文档查询功能 GET /api/documents/{id}。

背景：
当前项目是 ai-doc-summary，已经完成：
1. POST /api/documents 文档保存功能。
2. 第 8 课创建了文档查询功能的轻量 Spec：
   - specs/document-query/requirements.md
   - specs/document-query/design.md
   - specs/document-query/tasks.md
   - specs/document-query/test.md
3. 第 7A 课已经在 WORKFLOW.md 中沉淀了 Plan-Then-Act Tooling，要求每次只执行下一个未完成任务。

现在进入第 9 课：Spec 驱动实现文档查询功能。

输入：
请先读取以下文件：
1. specs/document-query/requirements.md
2. specs/document-query/design.md
3. specs/document-query/tasks.md
4. specs/document-query/test.md
5. AGENTS.md
6. CLAUDE.md
7. WORKFLOW.md
8. 当前 src/ 代码
9. 当前 git status

第一步：
请先不要修改代码。
请先输出 Spec 审查结果：

1. requirements.md、design.md、tasks.md、test.md 是否一致
2. 是否存在矛盾或遗漏
3. 是否存在过度设计
4. 是否符合当前课程边界
5. 你准备执行 tasks.md 中的哪一个未完成任务

如果 Spec 没有明显问题，再进入实现。

实现规则：

1. 严格按照 `specs/document-query/tasks.md` 逐项实现。
2. 每次只执行 `tasks.md` 中的下一个未完成 task。
3. 完成一个 task 后必须立即停止。
4. 不要一次性完成所有 task。
5. 不要提前执行后续 task。
6. 每完成一个 task 后，必须立即更新 `specs/document-query/tasks.md`：

   * 只把当前刚完成的 task 从 `- [ ]` 改为 `- [x]`
   * 不要勾选尚未执行的 task
   * 不要批量勾选多个 task
   * 不要重写整个 tasks.md
   * 只做最小必要修改
7. 更新 `tasks.md` 后，输出本次完成情况并等待我确认。
8. 等我确认后，才能继续下一个未完成 task。

每一步完成后输出：

1. 本次执行的是 `tasks.md` 中的哪一个 task。
2. 本次修改了哪些业务文件。
3. 是否更新了 `specs/document-query/tasks.md`。
4. `tasks.md` 中本次只勾选了哪一项。
5. 是否误勾选了其他未完成任务。
6. `git diff --stat` 摘要。
7. 是否修改 `pom.xml`。
8. 是否新增依赖。
9. 是否越界修改。
10. 下一步建议，但不要执行下一步。

重要限制：

* 当前 step 完成后，必须停止。
* 不要继续执行下一个 task。
* 不要在最后才统一勾选所有 task。
* 不要把未完成的 task 标记为完成。
* 如果某个 task 只完成了一部分，不要勾选它，应说明剩余内容。

功能约束：
1. 只实现 GET /api/documents/{id}。
2. 查询成功返回 documentId、title、content。
3. documentId 不存在时返回 404 Not Found。
4. 当前仍然只使用内存存储。
5. 不接数据库。
6. 不使用 JPA。
7. 不新增依赖。
8. 不接真实 AI API。
9. 不加入 Spring AI。
10. 不加入 Spring Security。
11. 不加入用户系统。
12. 不实现分页。
13. 不实现搜索。
14. 不实现文件上传。
15. 不实现摘要生成。

禁止事项：
1. 不要修改 pom.xml。
2. 不要新增依赖。
3. 不要修改 README.md。
4. 不要修改 AGENTS.md。
5. 不要修改 CLAUDE.md。
6. 不要修改 WORKFLOW.md。
7. 不要修改 COURSE.md。
8. 不要运行 mvn spring-boot:run。
9. 不要执行 git add。
10. 不要执行 git commit。
11. 不要让任何 Java 进程长期占用 8080。

测试要求：
根据 specs/document-query/test.md 添加或更新测试。
至少覆盖：
1. 查询已存在文档成功。
2. 查询不存在 documentId 返回 404。
3. 已有 POST /api/documents 测试不受影响。
4. 健康检查接口 GET /api/health 不受影响。

当执行到测试或最终验收 task 时：

1. 只在 `tasks.md` 中对应的测试 / 验收 task 被实际完成后，才把该 task 勾选为完成。
2. 如果 `mvn test` 还没有运行，不要勾选测试相关 task。
3. 如果 `git status` / `git diff --stat` 还没有检查，不要勾选验收相关 task。
4. 每个 task 都必须在完成当步后立即勾选，不允许最后统一批量勾选。
5. 最终所有 task 完成后，再输出整体总结。

验收标准：
1. GET /api/documents/{id} 可用。
2. 查询成功返回 documentId、title、content。
3. 查询不存在 documentId 返回 404 Not Found。
4. 仍然只使用内存存储。
5. 没有修改 pom.xml。
6. 没有新增依赖。
7. 没有引入数据库、JPA、Spring AI、真实 AI API、Security、用户系统。
8. 测试覆盖成功路径、404 路径和回归路径。
9. mvn test 通过。
10. specs/document-query/tasks.md 已反向更新。
```
