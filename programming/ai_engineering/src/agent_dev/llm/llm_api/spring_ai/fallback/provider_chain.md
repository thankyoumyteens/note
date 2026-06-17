# 显式 Provider 降级链

这是显式降级链。

```java
package com.example.llm.router;

import com.example.llm.client.AllProvidersFailedException;
import com.example.llm.client.LlmProviderClient;
import com.example.llm.client.LlmProviderException;
import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatResponse;

import java.util.ArrayList;
import java.util.List;

/**
 * 显式 provider fallback 降级链。
 * 只负责 provider 切换，不负责具体 provider API 调用。
 */
public class ProviderFallbackRouter {

    private final List<LlmProviderClient> clients;

    public ProviderFallbackRouter(List<LlmProviderClient> clients) {
        if (clients == null || clients.isEmpty()) {
            throw new IllegalArgumentException("clients must not be empty");
        }

        this.clients = List.copyOf(clients);
    }

    public UnifiedChatResponse chat(UnifiedChatRequest request) {
        List<LlmProviderException> failures = new ArrayList<>();

        for (LlmProviderClient client : clients) {
            try {
                return client.chat(request);

            } catch (LlmProviderException ex) {
                failures.add(ex);

                if (!shouldFallback(ex)) {
                    throw ex;
                }
            }
        }

        throw new AllProvidersFailedException(failures);
    }

    private boolean shouldFallback(LlmProviderException ex) {
        int status = ex.statusCode();

        return status == -1
                || status == 429
                || status == 500
                || status == 502
                || status == 503
                || status == 504;
    }
}
```

规则：

```text
400：不 retry，不 fallback
401：不 retry，不 fallback
403：默认不 retry，不 fallback
429：retry 后仍失败则 fallback
5xx：retry 后仍失败则 fallback
timeout / network error：retry 后仍失败则 fallback
```
