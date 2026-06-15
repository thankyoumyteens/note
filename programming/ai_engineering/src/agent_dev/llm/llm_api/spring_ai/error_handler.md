# 错误处理

Spring AI 里不能像 `WebClient.onStatus(...)` 那样直接写每个 HTTP 状态码处理。因为 HTTP 细节被 Spring AI 封装了。

Spring AI 的错误处理流程：

1. 捕获 Spring AI 异常
2. 用 @RestControllerAdvice 返回统一 JSON

```java
try {
    return chatClient.prompt()
            .user(message)
            .call()
            .content();

} catch (NonTransientAiException ex) {
    throw toLlmException(ex);

} catch (TransientAiException ex) {
    throw toLlmException(ex);

} catch (RuntimeException ex) {
    throw toLlmException(ex);
}
```

toLlmException：

```java
private LlmApiException toLlmException(RuntimeException ex) {
    HttpError httpError = findHttpError(ex);

    if (httpError != null) {
        return new LlmApiException(
                httpError.statusCode(),
                toProviderErrorCode(httpError.statusCode()),
                toSafeMessage(httpError.statusCode()),
                httpError.responseBody(),
                ex
        );
    }

    return new LlmApiException(
            500,
            "LLM_UNKNOWN_ERROR",
            "模型服务调用失败。",
            "",
            ex
    );
}

private String toProviderErrorCode(int statusCode) {
    return switch (statusCode) {
        case 400 -> "LLM_BAD_REQUEST";
        case 401 -> "LLM_UNAUTHORIZED";
        case 403 -> "LLM_FORBIDDEN";
        case 429 -> "LLM_RATE_LIMITED";
        default -> {
            if (statusCode >= 500) {
                yield "LLM_PROVIDER_SERVER_ERROR";
            }
            yield "LLM_API_ERROR";
        }
    };
}

private String toSafeMessage(int statusCode) {
    return switch (statusCode) {
        case 400 -> "模型请求参数错误，请检查 model、messages、max_tokens 等字段。";
        case 401 -> "模型服务认证失败，请检查 API Key。";
        case 403 -> "没有权限访问该模型或资源。";
        case 429 -> "模型服务限流或额度不足，请稍后重试。";
        default -> {
            if (statusCode >= 500) {
                yield "模型服务暂时不可用，请稍后重试。";
            }
            yield "模型服务调用失败。";
        }
    };
}

// Spring AI 抛出来的不一定直接就是 HTTP 异常；
// 所以要沿着 cause 链往里找 WebClientResponseException / RestClientResponseException。
private HttpError findHttpError(Throwable ex) {
    Throwable current = ex;

    while (current != null) {
        if (current instanceof WebClientResponseException webEx) {
            return new HttpError(
                    webEx.getStatusCode().value(),
                    webEx.getResponseBodyAsString()
            );
        }

        if (current instanceof RestClientResponseException restEx) {
            return new HttpError(
                    restEx.getRawStatusCode(),
                    restEx.getResponseBodyAsString()
            );
        }

        current = current.getCause();
    }

    return null;
}

private record HttpError(int statusCode, String responseBody) {
}
```

## 全局异常处理器返回统一 JSON

```java
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(LlmApiException.class)
    public ResponseEntity<ApiErrorResponse> handleLlmApiException(LlmApiException ex) {
        ApiErrorResponse body = new ApiErrorResponse(
                ex.code(),
                ex.safeMessage(),
                ex.upstreamStatus(),
                ex.upstreamBody()
        );

        return ResponseEntity
                .status(toClientStatus(ex.upstreamStatus()))
                .body(body);
    }

    private HttpStatus toClientStatus(int upstreamStatus) {
        return switch (upstreamStatus) {
            case 400 -> HttpStatus.BAD_REQUEST;
            case 429 -> HttpStatus.TOO_MANY_REQUESTS;
            case 401, 403 -> HttpStatus.BAD_GATEWAY;
            default -> {
                if (upstreamStatus >= 500) {
                    yield HttpStatus.BAD_GATEWAY;
                }
                yield HttpStatus.INTERNAL_SERVER_ERROR;
            }
        };
    }

    public record ApiErrorResponse(
            String code,
            String message,
            int upstreamStatus,
            String upstreamBody
    ) {
    }
}
```
