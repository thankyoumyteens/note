# 第 9 课：Spec 驱动实现文档查询功能

## 本课目标

本课正式实现：

```text
GET /api/documents/{id}
```

但和第 7 课不同，这一次不是单靠 prompt 控制 AI，而是要求 Codex **先读取 spec，再按 spec 实现**。

本课训练的是：

> **让 AI 以项目中的 spec 文件作为任务来源，而不是只依赖当前对话。**
