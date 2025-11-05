# 同步 GET 请求

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

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

            // 发送同步请求并获取响应
            HttpResponse<String> response = client.send(
                    request,
                    // 响应体处理器（转为 String）
                    HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8)
            );

            // 处理响应
            System.out.println("状态码：" + response.statusCode());
            System.out.println("响应体：" + response.body());
        }
    }
}
```
