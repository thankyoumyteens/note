# 第 10 课：先写测试，不写实现

前面你已经完成了：

```text
POST /api/documents
GET /api/documents/{id}
GET /api/documents/{id}/metadata
```

现在进入摘要功能：

```http
POST /api/documents/{id}/summary
```

但是第 10 课只做一件事：

```text
先写测试，不写实现。
```

也就是说，这节课的目标不是让接口跑通，而是让 AI 先把“摘要功能应该如何表现”写成测试。
