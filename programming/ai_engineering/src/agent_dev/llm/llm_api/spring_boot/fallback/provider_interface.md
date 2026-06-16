# 统一 ProviderClient 接口

```java
import reactor.core.publisher.Mono;

public interface LlmProviderClient {

    String provider();

    Mono<UnifiedChatResponse> chat(UnifiedChatRequest request);
}
```
