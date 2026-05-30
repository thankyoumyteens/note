# 为什么需要 Spec Workflow

普通 Plan-Then-Act 适合小功能，比如：

```text
POST /api/documents
```

但是当功能开始变复杂时，只靠一段 plan 容易丢上下文：

```text
需求是什么？
哪些不做？
接口怎么设计？
错误情况怎么处理？
测试覆盖什么？
任务完成到哪一步？
```

Spec Workflow 的作用是把这些内容拆成稳定的文件：

```text
specs/功能1/
  requirements.md
  design.md
  tasks.md
  test.md
```

这几个文件就像“功能级小文档”，后续 AI 实现时必须按它们执行，而不是自由发挥。

## 四个 Spec 文件分别干什么

### `requirements.md`

回答：

```text
这个功能要做什么？
不做什么？
验收标准是什么？
```

重点是 Scope 和 Non-goals。

例如：

```text
做：根据 documentId 查询已保存文档
不做：分页、搜索、数据库、权限、摘要、文件上传
```

---

### `design.md`

回答：

```text
接口怎么设计？
返回什么 JSON？
错误怎么处理？
涉及哪些类？
```

它偏技术设计，但仍然不写完整代码。

---

### `tasks.md`

回答：

```text
实现时分几步？
每一步做什么？
每一步是否完成？
```

它是后续第 9 课实现时的任务清单。

---

### `test.md`

回答：

```text
要测什么？
正常路径是什么？
异常路径是什么？
回归测试是什么？
```

它防止 AI 只写 happy path。
