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

## 为什么使用 WebClient

`WebClient` 是 Spring 生态常用 HTTP 客户端，适合调用外部模型 API。

本课用它完成：

```text
设置 base URL
设置 Authorization header
设置 Content-Type
发送 POST 请求
发送 JSON body
解析 JSON response
配置 timeout
```

Spring Framework 是 Java 企业应用常用基础框架，提供完整的编程和配置模型；本课程使用 Spring Boot + WebClient，是为了保持 Java 后端主线。
