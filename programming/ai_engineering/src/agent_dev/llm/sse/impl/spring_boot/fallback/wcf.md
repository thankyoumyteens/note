# WebClient 工厂：处理连接超时 + 响应超时

```java
package com.example.llm.provider;

import io.netty.channel.ChannelOption;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.netty.http.client.HttpClient;

import java.time.Duration;

/**
 * 创建带超时配置的 WebClient。
 * stream 场景下 responseTimeout 不要设置得太短，否则长回答可能被中间切断。
 */
public final class WebClientFactory {

    private WebClientFactory() {
    }

    public static WebClient create(
            String baseUrl,
            int connectTimeoutMillis,
            int responseTimeoutSeconds
    ) {
        HttpClient httpClient = HttpClient.create()
                // TCP 建连超时。
                .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, connectTimeoutMillis)
                // 等待 provider 响应的超时时间。
                .responseTimeout(Duration.ofSeconds(responseTimeoutSeconds));

        return WebClient.builder()
                .baseUrl(baseUrl)
                .clientConnector(new ReactorClientHttpConnector(httpClient))
                .build();
    }
}
```
