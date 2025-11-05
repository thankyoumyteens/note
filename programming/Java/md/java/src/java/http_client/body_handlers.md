# 响应体处理

HttpResponse.BodyHandlers 提供多种响应体处理器：

- ofString()：转为字符串
- ofFile(Path)：保存到文件
- ofByteArray()：转为字节数组
- discarding()：忽略响应体

## 示例（保存到文件）

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Path;
import java.nio.file.Paths;

public class SaveToFileDemo {
    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://httpbin.org/image/png"))
                .build();

        // 响应体保存到文件
        Path file = Paths.get("image.png");
        HttpResponse<Path> response = client.send(
                request,
                HttpResponse.BodyHandlers.ofFile(file)
        );

        System.out.println("文件保存路径: " + response.body());
    }
}
```
