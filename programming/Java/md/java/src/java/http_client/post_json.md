# POST 请求 json

```java
package com.example;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

public class PostFormDemo {
    public static void main(String[] args) throws Exception {
        try (
                // 创建 HttpClient（可配置超时、版本等）
                HttpClient client = HttpClient.newBuilder()
                        .connectTimeout(Duration.ofSeconds(10)) // 连接超时
                        .build()
        ) {
            // JSON 数据
            String jsonBody = "{\"name\":\"test\",\"age\":20}";

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://httpbin.org/post"))
                    // JSON 类型
                    .header("Content-Type", "application/json")
                    // POST 请求体
                    .POST(HttpRequest.BodyPublishers.ofString(jsonBody, StandardCharsets.UTF_8))
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            System.out.println("POST JSON 响应: " + response.body());
        }
    }
}
```
