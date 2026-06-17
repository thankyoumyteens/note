# 异常类

单个 provider 失败时：

```java
package com.example.llm.client;

/**
 * 单个 provider 调用失败时抛出的统一异常。
 * statusCode = -1 表示 timeout、网络异常、未知连接异常等没有 HTTP status 的错误。
 */
public class LlmProviderException extends RuntimeException {

    private final String provider;
    private final int statusCode;
    private final String responseBody;

    public LlmProviderException(
            String provider,
            int statusCode,
            String message,
            String responseBody,
            Throwable cause
    ) {
        super(message, cause);
        this.provider = provider;
        this.statusCode = statusCode;
        this.responseBody = responseBody == null ? "" : responseBody;
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
}
```

全部 provider 都失败时：

```java
package com.example.llm.client;

import java.util.List;

/**
 * 所有 provider 都失败时抛出。
 */
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
