# 第 8 课：轻量 Spec 结构

## 本课目标

你已经实现了第一个业务功能：

```text
POST /api/documents
```

现在要为第二个业务功能做准备：

```text
GET /api/documents/{id}
```

也就是：**根据 documentId 查询文档**。

但第 8 课仍然**不直接写代码**。这一课只做一件事：

> 为文档查询功能创建一组轻量 spec 文件。

## 为什么要引入 Spec Workflow

前面第 4～7 课，我们已经用 prompt 控制了一个小功能：

```text
文档保存功能
```

但随着功能变多，单靠聊天上下文会逐渐不稳定。比如后续会有：

```text
文档查询
文档摘要
Fake AI Client
真实 AI Provider
错误处理
测试
重构
```

如果所有规则都只放在对话里，AI 很容易忘记：

```text
这个功能做什么？
不做什么？
接口约束是什么？
要改哪些文件？
测试怎么验收？
```

所以从第 8 课开始，引入轻量 spec。

它不是传统的重型需求文档，而是给 AI coding agent 用的稳定上下文锚点。

## 本课要创建的目录结构

本课目标目录：

```text
specs/document-query/
  requirements.md
  design.md
  tasks.md
  test.md
```

每个功能都有自己的 spec 目录，本课放在 document-query 目录下。

四个文件分别负责：

```text
requirements.md  说明要做什么、不做什么、验收标准
design.md        说明怎么做、影响哪些文件、风险是什么
tasks.md         把实现拆成可执行小任务
test.md          说明测试计划和回归风险
```

第 8 课只创建 spec，不实现 `GET /api/documents/{id}`。

## 需求越来越多后，目录应该怎么组织？

不要把所有需求塞进一个大文件。

正确方式是：一个功能一个 spec 目录。

推荐结构：

```
specs/
  document-create/
    requirements.md
    design.md
    tasks.md
    test.md

  document-query/
    requirements.md
    design.md
    tasks.md
    test.md

  document-summary/
    requirements.md
    design.md
    tasks.md
    test.md

  ai-provider/
    requirements.md
    design.md
    tasks.md
    test.md
```

如果项目变大，可以额外加一个总索引：

```
specs/README.md
```

里面写：

```markdown
# Specs Index

## Active Specs

- document-query: implement GET /api/documents/{id}
- document-summary: implement POST /api/documents/{id}/summary

## Completed Specs

- document-create: implement POST /api/documents

## Project-wide Rules

- Do not change existing API response formats without explicit approval.
- All behavior changes require tests.
```

这样 AI 不需要每次读所有 spec，而是先看索引，再读当前任务相关 spec。
