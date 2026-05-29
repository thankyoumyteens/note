# 第 7 课：小步实现文档保存功能

第 6 课已经完成了 Plan。

第 7 课进入 Act，但不是让 AI 一口气随便改，而是：

```text
严格按照第 6 课计划
小步实现 POST /api/documents
每一步保持小 diff
最终运行 mvn test
检查 git diff
确认没有越界修改
```

最终要实现：

```http
POST /api/documents
```

请求：

```json
{
  "title": "Spring Boot 学习笔记",
  "content": "这是一篇关于 Spring Boot 最小项目的文档正文。"
}
```

成功响应：

```json
{
  "documentId": "1"
}
```

注意：成功响应第一版 **只返回 `documentId`**，不要返回 `title` 或 `content`。
