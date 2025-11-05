# POST 请求表单

post 的同步和异步与 get 类似。

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
            // 表单数据
            Map<String, String> formData = new HashMap<>();
            formData.put("name", "test");
            formData.put("age", "20");

            // 转换为 form-urlencoded 格式（key1=value1&key2=value2）
            String formBody = formData.entrySet().stream()
                    .map(entry -> entry.getKey() + "=" + entry.getValue())
                    .collect(Collectors.joining("&"));

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://httpbin.org/post"))
                    // 表单类型
                    .header("Content-Type", "application/x-www-form-urlencoded")
                    // POST 请求体
                    .POST(HttpRequest.BodyPublishers.ofString(formBody, StandardCharsets.UTF_8))
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            System.out.println("POST 表单响应: " + response.body());
        }
    }
}
```
