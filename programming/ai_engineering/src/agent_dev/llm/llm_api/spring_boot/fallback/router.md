# 显式 Provider 降级链

```java
import reactor.core.Exceptions;
import reactor.core.publisher.Mono;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeoutException;

public class ProviderFallbackRouter {

    private final List<LlmProviderClient> clients;

    public ProviderFallbackRouter(List<LlmProviderClient> clients) {
        this.clients = clients;
    }

    public Mono<UnifiedChatResponse> chat(UnifiedChatRequest request) {
        return callByIndex(request, 0, new ArrayList<>());
    }

    private Mono<UnifiedChatResponse> callByIndex(
            UnifiedChatRequest request,
            int index,
            List<LlmProviderException> failures
    ) {
        if (index >= clients.size()) {
            return Mono.error(new AllProvidersFailedException(failures));
        }

        LlmProviderClient client = clients.get(index);

        return client.chat(request)
                .onErrorResume(ex -> {
                    LlmProviderException providerException = toProviderException(client.provider(), ex);
                    failures.add(providerException);

                    if (!shouldFallback(providerException)) {
                        return Mono.error(providerException);
                    }

                    // 降级
                    return callByIndex(request, index + 1, failures);
                });
    }

    private boolean shouldFallback(LlmProviderException ex) {
        int status = ex.statusCode();

        return status == 429
                || status == 500
                || status == 502
                || status == 503
                || status == 504
                || status == -1;
    }

    private LlmProviderException toProviderException(String provider, Throwable throwable) {
        Throwable ex = Exceptions.unwrap(throwable);

        if (ex instanceof LlmProviderException providerException) {
            return providerException;
        }

        if (ex instanceof TimeoutException) {
            return new LlmProviderException(
                    provider,
                    -1,
                    "Provider timeout",
                    "",
                    ex
            );
        }

        return new LlmProviderException(
                provider,
                -1,
                "Provider request failed",
                "",
                ex
        );
    }
}
```

这里用 `statusCode = -1` 表示：

```text
没有 HTTP status 的异常：
- timeout
- connection refused
- DNS error
- network error
```
