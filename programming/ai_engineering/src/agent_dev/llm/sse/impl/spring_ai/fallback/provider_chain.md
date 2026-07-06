# 显式 Provider 降级链

```java id="snocxf"
package com.example.llm.router;

import com.example.llm.dto.StreamEventType;
import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatStreamEvent;
import com.example.llm.exceptions.AllProvidersFailedException;
import com.example.llm.exceptions.LlmProviderException;
import com.example.llm.provider.LlmStreamProviderClient;
import org.springframework.web.client.RestClientResponseException;
import org.springframework.web.reactive.function.client.WebClientRequestException;
import org.springframework.web.reactive.function.client.WebClientResponseException;
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
                    LlmProviderException providerException =
                            toProviderException(client.provider(), ex);

                    failures.add(providerException);

                    if (contentStarted.get()) {
                        return Flux.error(providerException);
                    }

                    if (!isFallbackable(providerException)) {
                        return Flux.error(providerException);
                    }

                    return callByIndex(request, index + 1, failures);
                });
    }

    private static boolean isFallbackable(LlmProviderException ex) {
        int status = ex.statusCode();

        return status == -1
                || status == 429
                || status == 500
                || status == 502
                || status == 503
                || status == 504;
    }

    private static LlmProviderException toProviderException(String provider, Throwable throwable) {
        Throwable ex = Exceptions.unwrap(throwable);

        // 已经是统一 provider 异常时直接返回。
        if (ex instanceof LlmProviderException providerException) {
            return providerException;
        }

        // WebClient HTTP 错误，通常包含 HTTP 状态码和响应体。
        if (ex instanceof WebClientResponseException webClientResponseException) {
            return new LlmProviderException(
                    provider,
                    webClientResponseException.getStatusCode().value(),
                    "Provider HTTP error",
                    webClientResponseException.getResponseBodyAsString(),
                    webClientResponseException
            );
        }

        // RestClient HTTP 错误，Spring AI 某些底层调用可能使用 RestClient。
        if (ex instanceof RestClientResponseException restClientResponseException) {
            return new LlmProviderException(
                    provider,
                    restClientResponseException.getStatusCode().value(),
                    "Provider HTTP error",
                    restClientResponseException.getResponseBodyAsString(),
                    restClientResponseException
            );
        }

        // Reactor timeout 或 stream idle timeout。
        if (ex instanceof TimeoutException) {
            return new LlmProviderException(
                    provider,
                    -1,
                    "Provider stream timeout",
                    "",
                    ex
            );
        }

        // 网络连接失败、DNS 失败、连接被拒绝等请求级异常。
        if (ex instanceof WebClientRequestException) {
            return new LlmProviderException(
                    provider,
                    -1,
                    "Provider network error",
                    "",
                    ex
            );
        }

        // 其它未知异常统一包装为 provider stream failed。
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
