# 第 6 课：先计划，后执行

## 本课目标

这一课仍然**不要让 AI 写代码**。

你的目标是训练一个非常重要的 AI coding agent 工作习惯：

> 复杂度稍高的任务，先让 AI 给计划；人审查计划；确认后再实现。

对于当前项目，本课要围绕同一个功能：

```text
POST /api/documents
```

让 Codex 输出一份更接近真实开发前置方案的实现计划。

## 为什么要 Plan-Then-Act

如果你直接说：

```text
帮我实现文档保存功能。
```

Codex 可能会直接修改很多文件：

```text
DocumentController
DocumentService
DocumentRepository
DocumentEntity
DTO
测试
README
pom.xml
```

问题是：它可能顺手加数据库、加依赖、改 README、扩大响应结构，甚至把前面定好的“只返回 documentId”改掉。

所以现在要先让它做这件事：

```text
请先不要改代码。
请先给出实现计划。
```

这一步的价值是：你可以在代码被修改前审查它的意图。
