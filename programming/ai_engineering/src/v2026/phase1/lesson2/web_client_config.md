# 创建 WebClient 配置

新建：

```text
config/WebClientConfig.java
```

代码：

```java
package com.example.aigateway.config;

import io.netty.channel.ChannelOption;
import java.time.Duration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;

@Configuration
public class WebClientConfig {

    @Bean
    public WebClient llmWebClient(LlmProperties properties) {
        // 模型 API 是外部服务，如果不设置超时，请求可能长时间占用线程。
        HttpClient httpClient = HttpClient.create()
                // 连接超时
                .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 10_000)
                // 响应超时
                .responseTimeout(Duration.ofSeconds(properties.getTimeoutSeconds()));

        return WebClient.builder()
                .baseUrl(properties.getBaseUrl())
                .clientConnector(new ReactorClientHttpConnector(httpClient))
                // 大多数模型 API 使用 Bearer Token 鉴权。
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + properties.getApiKey())
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();
    }
}
```

这里做了两件重要的事：

```text
1. 设置 baseUrl 和 Authorization header
2. 设置连接超时和响应超时
```

## 为什么用 WebClient？

`WebClient` 是 Spring 提供的 HTTP 客户端，适合调用外部 API。

本课使用它完成：

- 设置 base URL
- 设置 Authorization header
- 设置 Content-Type
- 发送 POST 请求
- 发送 JSON body
- 解析 JSON response
- 配置连接超时
- 配置响应超时

典型调用结构：

```java
ChatCompletionResponse response = llmWebClient.post()
        .uri("/v1/chat/completions")
        .bodyValue(request)
        .retrieve()
        .bodyToMono(ChatCompletionResponse.class)
        .block();
```

这段代码的含义：

```text
发送 POST 请求
-> 请求路径 /v1/chat/completions
-> 请求体是 request
-> 取回响应
-> 反序列化为 ChatCompletionResponse
-> 阻塞等待结果
```

当前使用 `.block()` 是为了简化同步接口。

后续流式输出会使用 `Flux`。
