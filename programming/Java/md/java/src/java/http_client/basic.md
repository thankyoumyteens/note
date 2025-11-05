# 基本使用

基本使用流程:

1. 创建 HttpClient 实例（可配置超时、版本等）
2. 构建 HttpRequest（指定 URL、方法、参数等）
3. 发送请求（同步用 send()，异步用 sendAsync()），通过 BodyHandler 处理响应体
