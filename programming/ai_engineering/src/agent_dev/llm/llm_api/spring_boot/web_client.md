# WebClient 简介

`WebClient` 是 Spring 里用于发送 HTTP 请求的客户端，主要来自 **Spring WebFlux**。调用 OpenAI / Qwen / Claude / DeepSeek 这些模型 API，本质上就是后端作为 HTTP client 去请求第三方服务，所以 `WebClient` 很适合这个场景。

`WebClient` 的特点是：

1. 支持非阻塞
2. 支持流式响应
3. 支持 Mono / Flux
4. 适合 SSE / streaming
5. 适合高并发外部 API 调用
6. 和 Spring WebFlux / Reactor 配合很好

## WebClient 和 RestTemplate / RestClient 的区别

Spring 现在有几个常见 HTTP client：

| 客户端         | 类型                           | 适合场景                             |
| -------------- | ------------------------------ | ------------------------------------ |
| `RestTemplate` | 老的同步阻塞客户端             | 老项目维护，不建议新项目主用         |
| `RestClient`   | 新的同步阻塞 fluent client     | 普通同步 HTTP 请求                   |
| `WebClient`    | reactive / non-blocking client | streaming、高并发、SSE、异步链式调用 |

## WebClient 的核心调用链

代码大概是这种结构：

```java
webClient.post()
        .uri("/messages")
        .bodyValue(request)
        .retrieve()
        .bodyToMono(ClaudeMessageResponse.class)
        .timeout(Duration.ofSeconds(60))
        .block();
```

## 创建 WebClient

### 方式一：直接创建

```java
WebClient webClient = WebClient.builder()
        .baseUrl("https://dashscope.aliyuncs.com/apps/anthropic/v1")
        .defaultHeader("x-api-key", apiKey)
        .defaultHeader("anthropic-version", "2023-06-01")
        .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
        .build();
```

- baseUrl: 请求基础地址
- defaultHeader: 每个请求默认带上的 header
- build: 构建不可变的 WebClient 实例

### 方式二：注入 `WebClient.Builder`

Spring Boot 项目里更推荐这样：

```java
@Service
public class LlmClient {

    private final WebClient.Builder webClientBuilder;

    public LlmClient(WebClient.Builder webClientBuilder) {
        this.webClientBuilder = webClientBuilder;
    }
}
```

然后每个 provider 构造自己的 client：

```java
WebClient webClient = webClientBuilder
        .baseUrl(config.baseUrl())
        .defaultHeader("x-api-key", config.apiKey())
        .defaultHeader("anthropic-version", "2023-06-01")
        .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
        .build();
```

这样做的好处是：

1. 可以复用 Spring Boot 默认配置
2. 方便统一加 filter
3. 方便统一配置 codec、timeout、日志
4. 方便测试替换

## `baseUrl` 和 `uri` 的关系

下面这段代码：

```java
WebClient webClient = webClientBuilder
        .baseUrl(config.baseUrl())
        .defaultHeader("x-api-key", config.apiKey())
        .defaultHeader("anthropic-version", "2023-06-01")
        .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
        .build();

webClient.post()
        .uri("/messages")
        .bodyValue(request)
        .retrieve()
        .bodyToMono(ClaudeMessageResponse.class)
        .timeout(Duration.ofSeconds(60))
        .block();
```

最终请求 URL 是：

```text
config.baseUrl + /messages
```

## 设置请求方法

常见方法：

```java
webClient.get()
webClient.post()
webClient.put()
webClient.delete()
```

调用大模型通常是：

```java
webClient.post()
```

## 设置请求体：`bodyValue`

```java
.bodyValue(request)
```

意思是：把 request 对象序列化成 JSON 请求体。

例如 Java record：

```java
public record ClaudeMessageRequest(
        String model,
        @JsonProperty("max_tokens") Integer maxTokens,
        String system,
        List<ClaudeMessage> messages
) {
}
```

会被 Jackson 转成 JSON：

```json
{
  "model": "qwen3.7-plus",
  "max_tokens": 1000,
  "system": "You are a helpful assistant.",
  "messages": [
    {
      "role": "user",
      "content": "你好"
    }
  ]
}
```

## `retrieve()`

```java
.retrieve()
```

表示：准备读取响应。

常见写法：

```java
.retrieve()
.bodyToMono(ResponseDto.class)
```

意思是：

1. 读取响应体
2. 反序列化成 ResponseDto
3. 返回 `Mono<ResponseDto>`

`Mono` 是 Reactor 里的类型，表示：未来会有 0 或 1 个结果。

所以 `Mono<ClaudeMessageResponse>` 可以理解成：一个异步的 ClaudeMessageResponse。

如果返回多个元素，比如 streaming，就会用：

```java
Flux<String>
```

`Flux` 表示：未来会有 0 到 N 个结果

简单记：

```text
Mono<T> = 一个结果
Flux<T> = 多个结果 / 流式结果
```

## `block()`

```java
.block()
```

意思是：把 reactive 异步调用变成同步等待。

```java
ClaudeMessageResponse response = webClient.post()
        .uri("/messages")
        .bodyValue(request)
        .retrieve()
        .bodyToMono(ClaudeMessageResponse.class)
        .timeout(Duration.ofSeconds(60))
        .block();
```

本来 `bodyToMono()` 返回的是：

```java
Mono<ClaudeMessageResponse>
```

调用 `.block()` 后，当前线程会等待 HTTP 请求完成，然后拿到真正的 ClaudeMessageResponse。

也就是说，`.block()` 让它变成了同步调用。

## `timeout`

```java
.timeout(Duration.ofSeconds(60))
```

意思是：如果 60 秒内没有结果，就中断这个 reactive pipeline，抛出 timeout 异常。

## 错误处理：为什么你应该加 `onStatus`

默认情况下，`retrieve()` 遇到 4xx / 5xx 会抛异常。问题是：如果不手动读取错误响应体，你看不到第三方返回的具体错误。

解决的方法：

```java
.retrieve()
.onStatus(
        HttpStatusCode::isError,
        clientResponse -> clientResponse.bodyToMono(String.class)
                .map(body -> new RuntimeException(
                        "LLM API error, status="
                                + clientResponse.statusCode()
                                + ", body="
                                + body
                ))
)
.bodyToMono(ClaudeMessageResponse.class)
```

`onStatus` 的作用是：

```text
当 HTTP status 是 4xx / 5xx 时，HttpStatusCode::isError 返回 true，
读取错误 body，
转换成你自己的异常。
```

这对调模型 API 非常重要，因为 OpenAI / Qwen / Claude 的错误信息通常都在 JSON body 里。

如果想捕获更详细的 HTTP 错误码，可以写多个 onStatus：

```java
.retrieve()
.onStatus(status -> status.value() == 400, clientResponse -> ...)
.onStatus(status -> status.value() == 401 || status.value() == 403, clientResponse -> ...)
.onStatus(HttpStatusCode::is5xxServerError, clientResponse -> ...)
.bodyToMono(ClaudeMessageResponse.class)
```

---

## `retrieve()` vs `exchangeToMono()`

大部分简单场景用：

```java
.retrieve()
```

如果你需要做更复杂处理，例如想拿到 status code、headers、body 等，就要用：

```java
.exchangeToMono(...)
```

例如：

```java
Mono<ClaudeMessageResponse> mono = webClient.post()
        .uri("/messages")
        .bodyValue(request)
        .exchangeToMono(response -> {
            if (response.statusCode().is2xxSuccessful()) {
                return response.bodyToMono(ClaudeMessageResponse.class);
            }

            return response.bodyToMono(String.class)
                    .flatMap(body -> Mono.error(new RuntimeException(
                            "LLM API error: " + body
                    )));
        })
        .timeout(Duration.ofSeconds(60))
        .block();
```

选择规则：

- 普通成功/失败处理：retrieve() + onStatus()
- 需要完全控制 response：exchangeToMono()

## Header 设置

调用不同厂商时，header 不一样。

### OpenAI / Qwen / DeepSeek OpenAI-compatible

```java
.defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + config.apiKey())
.defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
```

最终 HTTP header：

```http
Authorization: Bearer xxx
Content-Type: application/json
```

### Claude / Anthropic-compatible

```java
.defaultHeader("x-api-key", config.apiKey())
.defaultHeader("anthropic-version", "2023-06-01")
.defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
```

最终：

```http
x-api-key: xxx
anthropic-version: 2023-06-01
Content-Type: application/json
```
