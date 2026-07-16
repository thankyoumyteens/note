# 大模型 API 调用

这一章分为三层：

1. API 契约：理解 API 类型、消息、参数、响应和 API Key 安全。
2. 单 Provider 调用：从 WebClient、Spring AI、Python 中选择一条实现路线，分别调用三类 API。
3. 多 Provider 工程化：统一请求与响应 DTO，再加入超时、错误处理、重试、降级、延迟和调用记录。

WebClient 适合直接控制 HTTP 契约，Spring AI 适合使用 Java 统一抽象，Python 适合使用 Provider 官方 SDK。三条路线是同一知识点的不同实现，不需要混合成一套代码。

先完成单 Provider 调用；需要屏蔽 API 差异或支持 Provider 切换时，再进入统一契约、ProviderClient 和重试降级。
