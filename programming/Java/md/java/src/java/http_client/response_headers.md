# 获取响应头

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;

public class GetResponseHeaders {
    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(10))
                .build();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://httpbin.org/get"))
                .timeout(Duration.ofSeconds(10))
                .build();
        // 发送请求并获取响应
        HttpResponse<String> response = client.send(
                request,
                HttpResponse.BodyHandlers.ofString()
        );

        // 获取响应头（HttpHeaders 对象）
        HttpResponse.Headers headers = response.headers();


        // 方式 1：获取指定头的第一个值（如 Content-Type）
        Optional<String> contentType = headers.firstValue("Content-Type");
        contentType.ifPresent(value -> System.out.println("Content-Type: " + value));


        // 方式 2：获取指定头的所有值（如 Set-Cookie 可能有多个）
        List<String> setCookies = headers.allValues("Set-Cookie");
        System.out.println("\nSet-Cookie 所有值:");
        setCookies.forEach(cookie -> System.out.println("- " + cookie));


        // 方式 3：获取所有头的键值对映射
        Map<String, List<String>> headerMap = headers.map();
        System.out.println("\n所有响应头（键值对）:");
        headerMap.forEach((key, values) -> {
            System.out.print(key + ": ");
            System.out.println(values); // 每个 key 对应一个值列表
        });


        // 方式 4：获取所有头名称
        Set<String> headerNames = headers.names();
        System.out.println("\n所有头名称:");
        headerNames.forEach(name -> System.out.println("- " + name));
    }
}
```
