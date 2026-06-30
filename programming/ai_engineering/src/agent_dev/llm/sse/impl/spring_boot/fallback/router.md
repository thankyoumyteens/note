# 显式 Provider 降级链

```java
package com.example.llm.provider;


import com.example.llm.dto.StreamEventType;
import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatStreamEvent;
import com.example.llm.exceptions.AllProvidersFailedException;
import com.example.llm.exceptions.LlmProviderException;
import reactor.core.Exceptions;
import reactor.core.publisher.Flux;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeoutException;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * 显式 provider 降级链。
 * 只有在当前 provider 尚未输出 message chunk 时，才允许 fallback。
 */
public class StreamProviderFallbackRouter {

    private final List<LlmStreamProviderClient> clients;

    public StreamProviderFallbackRouter(List<LlmStreamProviderClient> clients) {
        if (clients == null || clients.isEmpty()) {
            throw new IllegalArgumentException("clients must not be empty");
        }

        this.clients = List.copyOf(clients);
    }

    public Flux<UnifiedChatStreamEvent> stream(UnifiedChatRequest request) {
        return callByIndex(request, 0, new ArrayList<>());
    }

    private Flux<UnifiedChatStreamEvent> callByIndex(
            UnifiedChatRequest request,
            int index,
            List<LlmProviderException> failures
    ) {
        if (index >= clients.size()) {
            return Flux.error(new AllProvidersFailedException(failures));
        }

        LlmStreamProviderClient client = clients.get(index);
        AtomicBoolean contentStarted = new AtomicBoolean(false);

        return client.stream(request)
                .doOnNext(event -> {
                    if (event.type() == StreamEventType.MESSAGE) {
                        contentStarted.set(true);
                    }
                })
                .onErrorResume(ex -> {
                    LlmProviderException providerException = toProviderException(client.provider(), ex);
                    failures.add(providerException);

                    if (contentStarted.get()) {
                        return Flux.error(providerException);
                    }

                    if (!shouldFallback(providerException)) {
                        return Flux.error(providerException);
                    }

                    return callByIndex(request, index + 1, failures);
                });
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

    private LlmProviderException toProviderException(String provider, Throwable throwable) {
        Throwable ex = Exceptions.unwrap(throwable);

        if (ex instanceof LlmProviderException providerException) {
            return providerException;
        }

        if (ex instanceof TimeoutException) {
            return new LlmProviderException(
                    provider,
                    -1,
                    "Provider stream timeout",
                    "",
                    ex
            );
        }

        return new LlmProviderException(
                provider,
                -1,
                "Provider stream failed",
                "",
                ex
        );
    }
}
```

## Stream 场景下为什么不能随便 fallback

非 stream 调用中，fallback 比较简单：

```text
Provider A 失败
  ↓
切 Provider B
  ↓
返回完整结果
```

但 stream 调用不同。

如果 Provider A 已经输出了前半段：

```text
RAG 是一种结合检索和生成的技术，
```

然后中途失败，再切 Provider B，Provider B 可能输出另一种风格、另一种内容：

```text
它通常由向量数据库、embedding 模型和生成模型组成
```

最终前端看到的回答可能来自两个模型：

```text
前半段来自 Provider A
后半段来自 Provider B
```

这是错误的。

所以 stream fallback 必须遵守：

```text
只有在尚未输出任何 message chunk 前，才允许 fallback
```
