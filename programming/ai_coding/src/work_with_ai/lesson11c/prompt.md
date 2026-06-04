# 使用组合 Skill 实战小功能

## 实战功能

```http
PATCH /api/documents/{id}/title
```

功能说明：

```text
只修改已保存文档的 title，不修改 content。
```

成功响应：

```json
{
  "documentId": "1",
  "title": "新的标题"
}
```

错误处理：

```text
documentId 不存在：404 Not Found
title 为空字符串：400 Bad Request
title 为纯空格：400 Bad Request
```

明确不做：

```text
不修改 content
不实现 PATCH /api/documents/{id}
不实现 updatedAt
不实现版本历史
不实现用户权限
不接数据库
不使用 JPA
不新增依赖
不接真实 AI API
不接 Spring AI
不加 Spring Security
不实现文件上传
不实现摘要相关新功能
```

---

## 给 Claude Code / Codex 的 Prompt

创建完 `spec-tdd-cycle` 后，你不需要再写长 prompt。直接发这个：

```text
目标：
使用 spec-tdd-cycle skill 实战。

请使用 spec-tdd-cycle skill。

功能：
PATCH /api/documents/{id}/title

要求：
只修改文档 title，不修改 content。

成功响应：
{
  "documentId": "1",
  "title": "新的标题"
}

错误处理：
1. documentId 不存在返回 404。
2. title 为空字符串返回 400。
3. title 为纯空格返回 400。

明确不做：
1. 不修改 content。
2. 不实现 PATCH /api/documents/{id}。
3. 不实现 updatedAt。
4. 不实现版本历史。
5. 不实现用户权限。
6. 不接数据库 / JPA。
7. 不新增依赖。
8. 不接真实 AI API。
9. 不接 Spring AI。
10. 不加 Security / 用户系统。

本轮只执行第 0 轮：状态检查与计划输出。
不要修改任何文件。
完成后停止，等待我确认。
```

---

## 后续每轮怎么继续

第 0 轮完成后，你只需要说：

```text
继续。按 spec-tdd-cycle skill 只执行下一轮唯一 task，完成后停止。
```

每一轮都重复这句话。

如果你想更明确一点：

```text
继续。只执行第 1 轮：创建或确认 MCP feature。完成后停止。
```

再下一轮：

```text
继续。只执行第 2 轮：requirements。完成后停止。
```

然后依次是：

```text
继续。只执行第 3 轮：design。完成后停止。
```

```text
继续。只执行第 4 轮：tasks。完成后停止。
```

```text
继续。只执行第 5 轮：TDD Red。完成后停止。
```

```text
继续。只执行第 6 轮：TDD Green。完成后停止。
```

```text
继续。只执行第 7 轮：TDD Refactor。完成后停止。
```

```text
继续。只执行第 8 轮：最终验收汇总。完成后停止。
```

---

## 如果 AI 一口气执行多个 task

直接发：

```text
停止。你违反了 spec-tdd-cycle skill 的 one-task-at-a-time gate。

不要继续修改任何文件。
请立即输出：
1. 你实际执行了哪些 round / task。
2. 哪些是未经我确认就执行的。
3. 当前 git status。
4. 当前 git diff --stat。
5. 当前 MCP task 状态。
6. 如何回到每次只执行一个 task 的状态。
```
