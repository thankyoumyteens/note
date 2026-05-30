# 第 9B 课：用 spec-workflow-mcp 做一个小功能

第 9A 课你已经完成了 `spec-workflow-mcp` 的安装、配置和基本理解。第 9B 课开始真正使用它做一个很小的功能。

本课目标不是做复杂业务，而是验证：

```text
spec-workflow-mcp 能不能更好地管理：
1. requirements
2. design
3. tasks
4. approval
5. progress tracking
6. implementation logs
```

实战功能建议：

```http
GET /api/documents/{id}/metadata
```

它足够小，但又能完整走一遍 Spec Workflow。
