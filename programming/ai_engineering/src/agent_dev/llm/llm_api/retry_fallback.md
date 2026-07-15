# 重试和 Provider 降级

重试是在同一个 Provider 内再次调用，降级是当前 Provider 重试耗尽后切换到下一个 Provider。

## 错误规则

| 错误 | 重试 | 降级 |
| --- | --- | --- |
| 400、401、403 | 否 | 否，立即返回当前错误 |
| 429 | 是 | 重试耗尽后降级 |
| 500、502、503、504 | 是 | 重试耗尽后降级 |
| 超时、连接和网络错误（`-1`） | 是 | 重试耗尽后降级 |
| 其他错误 | 否 | 否 |

## 次数

`maxRetries` 表示首次失败后的追加次数，因此单个 Provider 最多调用 `1 + maxRetries` 次。

如果有 `N` 个 Provider，全部返回可重试错误，整个降级链最多调用 `N × (1 + maxRetries)` 次。400、401、403 会立即终止，不再调用后续 Provider。

## 退避

三种实现都使用指数退避和随机抖动：初始等待约 500ms，逐次增长，最大约 3s。随机抖动用于避免大量请求同时重试。

| 实现 | 方式 |
| --- | --- |
| WebClient | Reactor `Retry.backoff` + `jitter` |
| Spring AI | 当前同步调用循环中计算退避和抖动 |
| Python + uv | Tenacity `wait_random_exponential` |

## 全部失败

只有所有 Provider 都因可降级错误耗尽时，Router 才抛出 `AllProvidersFailedException`，其中按调用顺序保存每个 Provider 的最终错误。
