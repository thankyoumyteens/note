# 错误处理

`retrieve()` 默认会把 4xx/5xx 转成 `WebClientResponseException`；如果要自定义错误处理，可以用 `onStatus`。

```java
return webClient.post()
        .uri(config.path())
        .bodyValue(body)
        .retrieve()
        .onStatus(
                status -> status.value() == 400,
                response -> toException(response, "Bad request: request body is invalid")
        )
        .onStatus(
                status -> status.value() == 401,
                response -> toException(response, "Unauthorized: API key is invalid or missing")
        )
        .onStatus(
                status -> status.value() == 403,
                response -> toException(response, "Forbidden: no permission to access this model or resource")
        )
        .onStatus(
                status -> status.value() == 429,
                response -> toException(response, "Rate limited: quota or request limit exceeded")
        )
        .onStatus(
                HttpStatusCode::is5xxServerError,
                response -> toException(response, "Provider server error")
        )
        .bodyToMono(ResponseDto.class);
```

错误转换方法：

```java
private Mono<? extends Throwable> toException(ClientResponse response, String message) {
    return response.bodyToMono(String.class)
            .defaultIfEmpty("")
            // 这里创建的异常，会在执行到 block() 时抛出
            .map(body -> new LlmApiException(
                    response.statusCode().value(),
                    message,
                    body
            ));
}
```

注意：多个 `onStatus` 会按顺序匹配。更具体的状态码要放前面，更宽泛的条件放后面。

## 加全局异常处理器捕获自定义的 LlmApiException 异常

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
                "LLM_API_ERROR",
                toSafeMessage(ex),
                ex.statusCode(),
                ex.responseBody()
        );

        return ResponseEntity
                .status(toClientStatus(ex.statusCode()))
                .body(body);
    }

    private HttpStatus toClientStatus(int upstreamStatus) {
        return switch (upstreamStatus) {
            case 400 -> HttpStatus.BAD_REQUEST;
            case 401, 403 -> HttpStatus.BAD_GATEWAY;
            case 429 -> HttpStatus.TOO_MANY_REQUESTS;
            default -> {
                if (upstreamStatus >= 500) {
                    yield HttpStatus.BAD_GATEWAY;
                }
                yield HttpStatus.INTERNAL_SERVER_ERROR;
            }
        };
    }

    private String toSafeMessage(LlmApiException ex) {
        return switch (ex.statusCode()) {
            case 400 -> "模型请求参数错误，请检查 model、messages、max_tokens 等字段。";
            case 401 -> "模型服务认证失败，请检查 API Key。";
            case 403 -> "没有权限访问该模型或资源。";
            case 429 -> "模型服务限流或额度不足，请稍后重试。";
            default -> "模型服务调用失败。";
        };
    }
}
```
