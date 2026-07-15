# 调用 OpenAI Responses API

当前项目使用 Spring AI 1.1.6，其 `ChatClient` / `ChatModel` 路线没有提供与 OpenAI `/responses` 原始契约对等的调用方式，因此不提供 Spring AI 实现。

这是当前项目和版本的限制，不代表 Spring AI 所有版本都不支持 Responses API。

Java 需要调用 Responses API 时，使用 [Spring Boot + WebClient](../spring_boot/responses_api.md)。该实现仍可接入[统一 ProviderClient](../provider_client.md)，不影响统一 DTO、Router 和降级链。
