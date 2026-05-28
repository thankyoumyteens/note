# 为什么必须先计划

如果你现在直接对 Claude Code 说：

```text
实现文档保存功能。
```

它可能会一次性改很多文件：

```text
DocumentController
DocumentService
DocumentRepository
DocumentEntity
GlobalExceptionHandler
pom.xml
README.md
测试文件
```

甚至可能顺手加入：

```text
JPA
H2
Spring Validation
Spring Security
Swagger
复杂异常体系
```

这会破坏课程当前的边界。

第 6 课要做的是先问清楚：

```text
你准备改哪些文件？
你准备新增哪些类？
你是否会修改 pom.xml？
你是否会新增依赖？
你是否还记得成功响应只返回 documentId？
你是否有测试计划？
如果失败怎么回滚？
```
