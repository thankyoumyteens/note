# 配置 Redis 和限流规则

生产级限流必须可配置。不同调用类型的成本不同，比如：

```text
CHAT：普通聊天
STREAM_CHAT：流式聊天，可能占用连接更久
TASK_EXTRACTION：结构化抽取
JSON_REPAIR：修复调用，通常不希望过多
TOOL_DECISION：工具调用决策
```

所以本课先按 `callType` 配置限流。

#### 代码

修改 `src/main/resources/application.yml`：

```yaml
spring:
  data:
    redis:
      host: localhost
      port: 6379

ai:
  rate-limit:
    enabled: true
    default-rule:
      limit: 60
      window-seconds: 60
    call-type-rules:
      CHAT:
        limit: 30
        window-seconds: 60
      STREAM_CHAT:
        limit: 10
        window-seconds: 60
      TASK_EXTRACTION:
        limit: 30
        window-seconds: 60
      JSON_REPAIR:
        limit: 20
        window-seconds: 60
      TOOL_DECISION:
        limit: 30
        window-seconds: 60
```

#### 代码说明

这里有两层规则：

```text
default-rule：默认限流规则
call-type-rules：按调用类型覆盖默认规则
```

例如 `STREAM_CHAT` 限制更低，是因为流式请求通常连接时间更长。
