# 第 10 课：Python AI 工具补齐

## 本课要解决什么问题

前面 1～9 课，你已经完成了 Java AI Gateway 的核心基础：

```text
普通聊天
流式输出
结构化输出
Function Calling
调用日志
限流 / 重试 / Fallback
Spring AI 可选接入
```

但 AI 应用开发中，有一类工作用 Python 更方便：

```text
文档解析
批处理脚本
模型调用实验
结构化输出实验
embedding 批处理
评估脚本
数据清洗
```

一句话概括本课：

> 本课补齐 Python 在 AI 应用开发中的辅助能力，让你能用 Python 做实验、解析、批处理和评估，但不改变 Java 后端主线。

## Python 的定位

Python 的定位是辅助工具：

```text
Java：生产级后端主服务
Python：AI 工具、文档处理、评估、批处理、实验
```

推荐分工：

```text
Spring Boot
  -> 用户接口
  -> 权限系统
  -> AI Gateway
  -> RAG API
  -> Agent API
  -> 审计日志
  -> 成本统计

Python scripts / workers
  -> 文档解析
  -> embedding 批处理
  -> eval dataset 构造
  -> RAGAS 评估
  -> prompt 实验
  -> 数据清洗
```

## Python 调模型 API 和 Java 调模型 API 的区别

本质一样，都是 HTTP API 调用。

Java 里你用了：

```text
WebClient
DTO
LlmClient
OpenAiCompatibleLlmClient
```

Python 里先用简单脚本：

```text
httpx
dict / Pydantic
OpenAI-compatible API
```

不要一上来引入 LangChain、LangGraph、LlamaIndex。

本课先掌握底层：

```text
Python -> HTTP -> OpenAI-compatible API -> JSON response -> Pydantic validation
```

这和你 Java 课程的底层逻辑一致。
