# 你应该期待的输出

## 合格的接口设计

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

错误响应：

```json
{
  "error": "title must not be blank"
}
```

状态码建议：

```text
201 Created：保存成功
400 Bad Request：title 或 content 非法
```

## 本课重点检查

你要检查 Claude Code 的输出是否符合这些要求：

```text
1. 有没有修改文件
2. 有没有严格输出任务说明和计划
3. 有没有使用 6 段式任务结构
4. 有没有明确 POST /api/documents
5. 请求字段是否是 title/content
6. 成功响应是否只返回 documentId
7. 是否坚持内存存储
8. 是否避免数据库、Spring AI、真实 AI API、Security、用户系统
9. 是否包含测试计划
10. 是否拆成后续小步实现任务
```

尤其注意：

```text
成功响应不要返回完整 content
```

因为第一版接口应该尽量小。
