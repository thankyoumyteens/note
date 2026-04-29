# 第 1 课：先建立 AI Gateway 的工程模型

今天先不急着写复杂代码。先明确你要构建的系统边界。

## 1. 普通后端接口长这样

传统 Java 后端一般是：

```text
Controller
  ↓
Service
  ↓
Repository
  ↓
Database
```

例如：

```text
GET /api/orders/123
  ↓
查数据库
  ↓
返回订单 JSON
```

这是确定性的。

---

## 2. AI Gateway 长这样

AI 应用后端更像：

```text
Controller
  ↓
AI Service
  ↓
Prompt Builder
  ↓
Model Client
  ↓
LLM Provider
  ↓
Response Validator
  ↓
返回结果
```

例如：

```text
POST /api/ai/chat
  ↓
构造 messages
  ↓
调用模型
  ↓
校验模型输出
  ↓
记录日志
  ↓
返回答案
```

核心区别是：**AI Gateway 不是简单代理模型 API，而是要把模型的不确定输出变成稳定的软件接口。**
