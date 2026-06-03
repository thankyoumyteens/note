# 第 14 课：权限隔离 RAG

当前 RAG 有一个严重问题：

```text
所有用户都可能检索到所有文档。
```

企业知识库不能这样做。不同租户、部门、用户应该只能检索自己有权限的文档。

一句话概括：

> 本课给 RAG 加上 tenantId / userId / visibility / allowedRoles / allowedUsers 权限字段，并在检索阶段通过 metadata filtering 防止越权检索。
