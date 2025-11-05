# 异步 GET 请求

```java
package com.example;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.concurrent.CompletableFuture;

public class HttpClientDemo {
    public static void main(String[] args) throws Exception {
        try (
                // 创建 HttpClient（可配置超时、版本等）
                HttpClient client = HttpClient.newBuilder()
                        .connectTimeout(Duration.ofSeconds(10)) // 连接超时
                        .build()
        ) {

            // 构建 GET 请求
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://api.animechan.io/v1/quotes/random?anime=naruto"))
                    // 设置请求头
                    .header("Accept", "application/json")
                    .GET() // 默认GET方法，可省略
                    .build();

            // 发送异步请求（返回 CompletableFuture）
            CompletableFuture<HttpResponse<String>> future = client.sendAsync(
                    request,
                    HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8)
            );

            // 处理异步结果（回调）
            future.thenAccept(response -> {
                System.out.println("异步状态码: " + response.statusCode());
                System.out.println("异步响应体: " + response.body());
            }).exceptionally(e -> { // 异常处理
                e.printStackTrace();
                return null;
            });

            // 等待异步完成（实际业务中可省略，避免阻塞）
            future.join();
        }
    }
}
```
