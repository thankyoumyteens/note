# 响应延迟

统一使用毫秒和单调时钟统计耗时。

| 字段 | 含义 |
| --- | --- |
| `providerLatencyMs` | 最终成功 ProviderClient 的完整耗时，包含其内部重试和退避 |
| `totalLatencyMs` | Router 整个调用耗时，包含失败 Provider、重试、退避和降级 |

没有发生降级时两者接近；发生降级时 `totalLatencyMs` 大于最终 Provider 的 `providerLatencyMs`。

WebClient 使用 Reactor `elapsed()`，Spring AI 使用 `System.nanoTime()`，Python 使用 `time.perf_counter()`；这些时钟不受系统时间调整影响。
