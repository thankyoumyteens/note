# 自定义异常

## 单个 provider 失败时的异常

```java
package com.example.llm.exceptions;

public class LlmProviderException extends RuntimeException {

    private final String provider;
    private final int statusCode;
    private final String responseBody;
    private final int retryCount;

    public LlmProviderException(
            String provider,
            int statusCode,
            String message,
            String responseBody,
            Throwable cause,
            int retryCount
    ) {
        super(message, cause);
        this.provider = provider;
        this.statusCode = statusCode;
        this.responseBody = responseBody == null ? "" : responseBody;
        this.retryCount = retryCount;
    }

    public LlmProviderException(
            String provider,
            int statusCode,
            String message,
            String responseBody,
            Throwable cause
    ) {
        this(provider, statusCode, message, responseBody, cause, 0);
    }

    public LlmProviderException(
            String provider,
            int statusCode,
            String message,
            String responseBody
    ) {
        this(provider, statusCode, message, responseBody, null);
    }

    public String provider() {
        return provider;
    }

    public int statusCode() {
        return statusCode;
    }

    public String responseBody() {
        return responseBody;
    }

    public int retryCount() {
        return retryCount;
    }
}
```

## 全部 provider 都失败时的异常

```java
package com.example.llm.exceptions;

import java.util.List;

public class AllProvidersFailedException extends RuntimeException {

    private final List<LlmProviderException> failures;

    public AllProvidersFailedException(List<LlmProviderException> failures) {
        super("All LLM providers failed");
        this.failures = List.copyOf(failures);
    }

    public List<LlmProviderException> failures() {
        return failures;
    }
}
```
