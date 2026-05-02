# 本课重点理解

你现在已经从 Mock 进入真实 AI 调用了。

这一课真正重要的不是“能调用模型”，而是这几个工程习惯：

## 1. API Key 不写死

错误：

```java
String apiKey = "sk-xxxx";
```

正确：

```yaml
api-key: ${OPENAI_API_KEY}
```

## 2. 业务层不绑定供应商

错误：

```java
OrderService 里面直接调用 OpenAI
```

正确：

```text
OrderService -> LlmClient -> OpenAiCompatibleLlmClient
```

## 3. 必须设置超时

模型 API 不是数据库本地查询，可能慢、可能断、可能限流。

生产系统必须考虑：

```text
connect timeout
read timeout
response timeout
retry
fallback
rate limit
```

## 4. 错误信息要可诊断

你至少要知道：

```text
是 API Key 错
是模型名错
是 quota 不够
是请求格式错
是超时
还是供应商返回 500
```
