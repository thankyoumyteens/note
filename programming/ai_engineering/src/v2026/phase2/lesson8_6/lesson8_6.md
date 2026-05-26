# 第 8.6 课：生产级日志、Tracing 与可观测性

第 8 课已经做了内存版日志：

```text
LlmCallLogService
ToolCallLogService
```

但它们有明显限制：

```text
服务重启后日志丢失
多实例部署时无法统一查询
无法长期统计 latency / token usage
无法通过 traceId 定位一次完整请求链路
```

一句话概括：

> 本课把内存日志升级为数据库持久化日志，并引入 requestId / traceId，为后续 LLMOps、告警、成本报表和白盒 eval 打基础。

本课不做：

```text
完整 LLMOps Dashboard
Prometheus / Grafana 实战接入
OpenTelemetry 全链路接入
A/B Test
Prompt Registry
完整 token budget 拦截
```
