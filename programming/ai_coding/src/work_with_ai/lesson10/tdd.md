# 什么是 TDD

TDD 是 **Test-Driven Development**，中文一般叫 **测试驱动开发**。

核心意思是：

> **先写测试，再写实现代码。**

不是先把功能写出来，再补测试。

---

## TDD 的基本流程

TDD 通常分 3 步：

```text
Red → Green → Refactor
```

### 1. Red：先写一个失败的测试

先写测试，描述你希望功能应该怎么表现。

比如你要实现：

```http
POST /api/documents/{id}/summary
```

你先写测试断言：

```text
调用 summary 接口应该返回 200
响应里应该有 documentId
响应里应该有 summary
```

因为接口还没实现，所以测试应该失败。

这就是 **Red**。

---

### 2. Green：写最小实现，让测试通过

然后你只写刚好够用的实现代码，让测试通过。

不是顺手重构，不是加复杂架构，不是引入数据库，也不是接真实 AI API。

例如：

```text
写一个 SummaryController
用 FakeAiSummaryClient 返回固定摘要
让测试通过
```

这就是 **Green**。

---

### 3. Refactor：在测试保护下重构

测试通过后，再看代码是否需要清理：

```text
重复代码能不能减少？
Controller 是否太重？
命名是否清楚？
异常处理是否合理？
```

重构后继续跑测试，保证行为没变。

这就是 **Refactor**。

---

## 为什么 TDD 适合 AI 编程

因为 AI 很容易：

```text
看起来写得很完整
但实际需求没覆盖
只测 happy path
测试跟着实现走
偷偷扩大范围
```

TDD 可以反过来控制 AI：

```text
先把行为写进测试
再让 AI 按测试实现
```

这样 AI 不是自由发挥，而是被测试约束。

---

## 当前课程里的 TDD 是什么

第 10 课是：

```text
先写测试，不写实现
```

也就是 TDD 的 **Red 阶段**。

第 11 课是：

```text
最小实现让测试通过
```

也就是 TDD 的 **Green 阶段**。

后面重构课才更接近 **Refactor 阶段**。
