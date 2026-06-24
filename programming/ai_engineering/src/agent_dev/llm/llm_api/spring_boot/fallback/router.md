# 显式 Provider 降级链

```java
package com.example.llm.provider;

import com.example.llm.exceptions.AllProvidersFailedException;
import com.example.llm.exceptions.LlmProviderException;
import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatResponse;
import reactor.core.Exceptions;
import reactor.core.publisher.Mono;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeoutException;

/**
 * Provider 降级路由器。
 * 按 clients 的顺序依次调用 provider，当前 provider 失败且允许降级时，继续调用下一个 provider。
 */
public class ProviderFallbackRouter {

    // 按优先级排序的 provider client 列表，例如 openai -> deepseek -> anthropic。
    private final List<LlmProviderClient> clients;

    public ProviderFallbackRouter(List<LlmProviderClient> clients) {
        this.clients = clients;
    }

    /**
     * 发起统一聊天请求。
     * 从第 0 个 provider 开始尝试，并记录每个失败的 provider 异常。
     */
    public Mono<UnifiedChatResponse> chat(UnifiedChatRequest request) {
        return callByIndex(request, 0, new ArrayList<>());
    }

    /**
     * 按 index 递归调用 provider。
     * 当前 provider 成功则直接返回；失败且允许降级则继续尝试下一个 provider。
     */
    private Mono<UnifiedChatResponse> callByIndex(
            UnifiedChatRequest request,
            int index,
            List<LlmProviderException> failures
    ) {
        // 所有 provider 都尝试失败后，抛出聚合异常，方便上层查看完整失败链路。
        if (index >= clients.size()) {
            return Mono.error(new AllProvidersFailedException(failures));
        }

        // 获取当前要尝试的 provider client。
        LlmProviderClient client = clients.get(index);

        return client.chat(request)
                .onErrorResume(ex -> {
                    // 将任意异常统一转换成 LlmProviderException，便于统一判断是否降级。
                    LlmProviderException providerException = toProviderException(client.provider(), ex);

                    // 记录当前 provider 的失败原因，最终所有 provider 失败时用于排查。
                    failures.add(providerException);

                    // 不允许降级的错误直接抛出，例如 400 / 401 / 403。
                    if (!shouldFallback(providerException)) {
                        return Mono.error(providerException);
                    }

                    // 允许降级的错误继续尝试下一个 provider。
                    return callByIndex(request, index + 1, failures);
                });
    }

    /**
     * 判断当前异常是否允许降级。
     * 只对临时性错误降级，不对参数错误、认证错误、权限错误降级。
     */
    private boolean shouldFallback(LlmProviderException ex) {
        int status = ex.statusCode();

        return status == 429 // 限流或额度临时不足。
                || status == 500 // provider 内部错误。
                || status == 502 // 网关错误。
                || status == 503 // provider 暂时不可用。
                || status == 504 // provider 响应超时。
                || status == -1; // 本地网络错误、连接错误或超时等非 HTTP 状态错误。
    }

    /**
     * 将不同类型的异常统一包装成 LlmProviderException。
     * 这样 fallback 判断和上层异常处理都只需要面向一个异常模型。
     */
    private LlmProviderException toProviderException(String provider, Throwable throwable) {
        // Reactor 可能会包装异常，这里先拆出原始异常。
        Throwable ex = Exceptions.unwrap(throwable);

        // 如果已经是统一异常，直接复用，避免重复包装丢失 statusCode 和 responseBody。
        if (ex instanceof LlmProviderException providerException) {
            return providerException;
        }

        // 请求超时没有 HTTP 状态码，用 -1 表示本地调用失败。
        if (ex instanceof TimeoutException) {
            return new LlmProviderException(
                    provider,
                    -1,
                    "Provider timeout",
                    "",
                    ex
            );
        }

        // 其它未知异常统一包装为 provider request failed。
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
