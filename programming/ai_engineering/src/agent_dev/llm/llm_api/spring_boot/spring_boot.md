# WebClient

这条路线直接处理 HTTP 请求和 Provider 原始契约，适合需要完整控制 endpoint、Header、请求体、响应和错误的场景。

基础 Demo 分别调用三类 API；掌握协议差异后，再进入错误处理和 fallback，将重复的协议转换收敛到 ProviderClient，并由 Router 统一处理重试、降级、耗时和调用记录。
