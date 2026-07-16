# 显式 Provider 降级链

这是显式降级链。

```java
package com.example.llm.router;

import com.example.llm.dto.UnifiedChatRequest;
import com.example.llm.dto.UnifiedChatResponse;
import com.example.llm.dto.LlmCallRecord;
import com.example.llm.dto.ProviderAttemptRecord;
import com.example.llm.exceptions.AllProvidersFailedException;
import com.example.llm.exceptions.LlmProviderException;
import com.example.llm.provider.LlmProviderClient;
import com.example.llm.recorder.LlmCallRecorder;
import com.example.llm.dto.LlmProvider;
import com.example.llm.dto.TokenUsage;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

/**
 * 显式 provider fallback 降级链。
 * 只负责 provider 切换，不负责具体 provider API 调用。
 */
public class ProviderFallbackRouter {

    private final List<LlmProviderClient> clients;
    private final LlmCallRecorder recorder;

    public ProviderFallbackRouter(List<LlmProviderClient> clients, LlmCallRecorder recorder) {
        if (clients == null || clients.isEmpty()) {
            throw new IllegalArgumentException("clients must not be empty");
        }

        this.clients = List.copyOf(clients);
        this.recorder = recorder;
    }

    public UnifiedChatResponse chat(UnifiedChatRequest request) {
        long totalStartNanos = System.nanoTime();
        Instant startedAt = Instant.now();
        List<LlmProviderException> failures = new ArrayList<>();
        List<ProviderAttemptRecord> attempts = new ArrayList<>();

        for (LlmProviderClient client : clients) {
            long providerStartNanos = System.nanoTime();
            Instant providerStartedAt = Instant.now();

            try {
                UnifiedChatResponse response = client.chat(request);
                long providerLatencyMs = elapsedMillis(providerStartNanos);
                attempts.add(successAttempt(client, response, providerStartedAt, providerLatencyMs));

                UnifiedChatResponse result = response.withLatency(
                        providerLatencyMs,
                        elapsedMillis(totalStartNanos)
                );
                save(successRecord(request, startedAt, result, attempts));
                return result;

            } catch (LlmProviderException ex) {
                failures.add(ex);
                attempts.add(failedAttempt(client, ex, providerStartedAt, elapsedMillis(providerStartNanos)));

                if (!shouldFallback(ex)) {
                    save(failedRecord(request, startedAt, elapsedMillis(totalStartNanos), attempts, ex));
                    throw ex;
                }
            }
        }

        AllProvidersFailedException ex = new AllProvidersFailedException(failures);
        save(failedRecord(request, startedAt, elapsedMillis(totalStartNanos), attempts, ex));
        throw ex;
    }

    private long elapsedMillis(long startNanos) {
        return (System.nanoTime() - startNanos) / 1_000_000;
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

    private ProviderAttemptRecord successAttempt(
            LlmProviderClient client,
            UnifiedChatResponse response,
            Instant startedAt,
            long latencyMs
    ) {
        return new ProviderAttemptRecord(
                response.provider(),
                response.model(),
                startedAt,
                Instant.now(),
                "SUCCESS",
                retryCount(response),
                latencyMs,
                null,
                null
        );
    }

    private ProviderAttemptRecord failedAttempt(
            LlmProviderClient client,
            LlmProviderException error,
            Instant startedAt,
            long latencyMs
    ) {
        return new ProviderAttemptRecord(
                LlmProvider.valueOf(client.provider().toUpperCase()),
                "",
                startedAt,
                Instant.now(),
                "FAILED",
                error.retryCount(),
                latencyMs,
                error.getClass().getSimpleName(),
                error.statusCode()
        );
    }

    private int retryCount(UnifiedChatResponse response) {
        return ((Number) response.metadata().getOrDefault("retryCount", 0)).intValue();
    }

    private LlmCallRecord successRecord(
            UnifiedChatRequest request,
            Instant startedAt,
            UnifiedChatResponse response,
            List<ProviderAttemptRecord> attempts
    ) {
        return new LlmCallRecord(
                (String) request.metadata().get("requestId"),
                (String) request.metadata().get("traceId"),
                startedAt,
                Instant.now(),
                "SUCCESS",
                response.provider(),
                response.model(),
                response.usage(),
                response.totalLatencyMs(),
                attempts.stream().map(ProviderAttemptRecord::provider).toList(),
                List.copyOf(attempts),
                null,
                null
        );
    }

    private LlmCallRecord failedRecord(
            UnifiedChatRequest request,
            Instant startedAt,
            long totalLatencyMs,
            List<ProviderAttemptRecord> attempts,
            Throwable error
    ) {
        LlmProviderException finalError = error instanceof AllProvidersFailedException all
                && !all.failures().isEmpty()
                ? all.failures().getLast()
                : error instanceof LlmProviderException providerError ? providerError : null;

        return new LlmCallRecord(
                (String) request.metadata().get("requestId"),
                (String) request.metadata().get("traceId"),
                startedAt,
                Instant.now(),
                "FAILED",
                null,
                null,
                TokenUsage.empty(),
                totalLatencyMs,
                attempts.stream().map(ProviderAttemptRecord::provider).toList(),
                List.copyOf(attempts),
                finalError == null ? error.getClass().getSimpleName() : finalError.getClass().getSimpleName(),
                finalError == null ? -1 : finalError.statusCode()
        );
    }

    private void save(LlmCallRecord record) {
        try {
            recorder.save(record);
        } catch (RuntimeException ignored) {
            // 记录失败不改变模型调用结果。
        }
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
