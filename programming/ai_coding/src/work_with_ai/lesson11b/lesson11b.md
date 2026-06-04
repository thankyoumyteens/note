# 第 11B 课：测试工作流工具化

第 10～11A 课已经完成了完整 TDD 闭环：

```text
第 10 课：Red，先写失败测试
第 11 课：Green，最小实现让测试通过
第 11A 课：Refactor，在测试保护下小步重构
```

第 11B 课要做的是：

```text
把 TDD 的 Red / Green / Refactor 固化成 skills/
```

本课产物应该是：

```text
skills/
  tdd-red/
    SKILL.md
  tdd-green/
    SKILL.md
  tdd-refactor/
    SKILL.md
```

可选：

```text
skills/
  tdd-cycle/
    SKILL.md
```

`WORKFLOW.md` 只保留简短索引和选择规则，不写长篇执行细节。

## 为什么本课用 Skill，而不是 WORKFLOW.md

`WORKFLOW.md` 适合做：

```text
工作流索引
选择规则
少量总原则
```

不适合继续塞：

```text
完整 prompt
长篇执行步骤
大量检查清单
每个阶段的详细行为约束
```

这些更适合放到 Skill：

```text
skills/tdd-red/SKILL.md
skills/tdd-green/SKILL.md
skills/tdd-refactor/SKILL.md
```

这样后续你可以直接让 AI：

```text
请使用 tdd-red skill 为这个功能先写失败测试。
```

而不是每次复制一大段 prompt。

## 三个 Skill 的职责

### `tdd-red`

用途：

```text
只写测试，不写实现。
```

它要约束 AI：

```text
1. 先理解需求
2. 只修改测试文件
3. 不修改 src/main/java
4. 写完后运行测试
5. 确认失败原因是功能尚未实现
6. 不允许为了通过测试而提前写实现
```

---

### `tdd-green`

用途：

```text
写最小实现，让已有失败测试通过。
```

它要约束 AI：

```text
1. 先读取失败测试
2. 不降低测试断言
3. 不删除测试
4. 只写最小业务代码
5. 不扩大功能范围
6. 运行 mvn test
7. 确认所有测试通过
```

---

### `tdd-refactor`

用途：

```text
在测试保护下小步重构。
```

它要约束 AI：

```text
1. 先评估是否需要重构
2. 不为了改而改
3. 不新增业务功能
4. 不改变 API 行为
5. 不降低测试断言
6. 每步重构后运行测试
7. 测试失败时停止并分析原因
```
