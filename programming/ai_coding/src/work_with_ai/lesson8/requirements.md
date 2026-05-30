# 你要检查 Spec 是否合格

## `requirements.md` 要检查

必须有：

```text
做什么
不做什么
验收标准
```

尤其要有 Non-goals：

```text
不接数据库
不做搜索
不做分页
不做权限
不做摘要
```

---

## `design.md` 要检查

成功响应这次应该返回完整文档：

```json
{
  "documentId": "1",
  "title": "Spring Boot 学习笔记",
  "content": "这是一篇关于 Spring Boot 最小项目的文档正文。"
}
```

注意：这和 `POST /api/documents` 不一样。

`POST` 成功只返回：

```json
{
  "documentId": "1"
}
```

`GET` 查询成功可以返回：

```json
{
  "documentId": "1",
  "title": "...",
  "content": "..."
}
```

---

## `tasks.md` 要检查

不要让它写成一个大任务：

```markdown
- [ ] 实现文档查询功能
```

这太粗。

应该类似：

```markdown
- [ ] 检查现有文档保存功能和内存存储结构
- [ ] 为 InMemoryDocumentStore 增加按 id 查询能力
- [ ] 新增查询响应 DTO
- [ ] 在 DocumentController 中新增 GET /api/documents/{id}
- [ ] 处理 documentId 不存在时的 404 响应
- [ ] 新增 MockMvc 测试覆盖查询成功
- [ ] 新增 MockMvc 测试覆盖文档不存在
- [ ] 运行 mvn test 并检查 git diff
```

---

## `test.md` 要检查

至少包含：

```text
查询已存在文档成功
查询不存在 documentId 返回 404
健康检查接口不受影响
已有 POST /api/documents 测试不受影响
```
