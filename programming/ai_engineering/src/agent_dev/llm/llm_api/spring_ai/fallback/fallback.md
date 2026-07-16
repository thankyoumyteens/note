# 重试和降级

Spring AI 的 ProviderClient 负责单个 Provider 的请求总超时、错误归一化和内部重试；ProviderFallbackRouter 在当前 Provider 重试耗尽后切换到下一个 Provider。

这里使用同步调用链：重试采用指数退避和随机抖动，Router 按配置顺序降级，并统一记录最终响应、失败链路、耗时和调用结果。
