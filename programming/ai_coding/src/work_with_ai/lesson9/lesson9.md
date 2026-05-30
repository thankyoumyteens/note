# 第 9 课：Spec 驱动实现文档查询功能

第 8 课你已经创建了轻量 Spec：

```text
specs/document-query/
  requirements.md
  design.md
  tasks.md
  test.md
```

第 9 课要做的是：

```text
让 AI 先读取 Spec
检查 Spec 是否矛盾
然后按 tasks.md 逐项实现
最后运行测试并反向更新 tasks.md
```

实战功能是：

```http
GET /api/documents/{id}
```

成功响应：

```json
{
  "documentId": "1",
  "title": "Spring Boot 学习笔记",
  "content": "这是一篇关于 Spring Boot 最小项目的文档正文。"
}
```

不存在时：

```http
404 Not Found
```
