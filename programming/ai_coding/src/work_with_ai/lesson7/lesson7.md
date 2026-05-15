# 第 7 课：小步实现文档保存功能

## 本课目标

这一课正式进入 **Act**，也就是让 Codex 开始改代码。

但重点不是“让 AI 一次性写完功能”，而是训练：

> **把一个功能拆成多个小 diff，让 AI 每次只完成一个小任务。**

文档保存功能最终要实现：

```text
POST /api/documents
```

请求：

```json
{
  "title": "Spring Boot 学习笔记",
  "content": "这是一篇文档正文。"
}
```

成功响应：

```json
{
  "documentId": "1"
}
```

核心约束继续保持：

```text
不接数据库
不接 AI API
不加用户系统
不加 Spring Security
不新增依赖
不实现查询接口
不实现摘要接口
成功响应只返回 documentId
```

## 为什么不能一次性让 Codex 实现

你可以直接说：

```text
按计划实现文档保存功能。
```

但这样 Codex 可能一次性改很多文件。如果中间混入了不该有的东西，比如改了 `pom.xml`、返回了完整 `content`、顺手更新了 README，你就很难定位是哪一步引入的问题。

所以第 7 课要求：

```text
一次只做一个小任务
每一步后检查 diff
每一步后运行相关测试或至少说明测试状态
发现偏离立刻纠正
```

这就是小步实现。

---

## 推荐任务拆分

建议按这个顺序：

```text
Step 1：新增 document 包和基础模型
Step 2：新增请求/响应 DTO
Step 3：新增内存存储 InMemoryDocumentStore
Step 4：新增 DocumentController
Step 5：新增或更新测试
Step 6：运行 mvn test 并修复问题
Step 7：检查 git diff
```

注意：第 7 课可以允许 Codex 修改代码，但每次改动范围要小。
