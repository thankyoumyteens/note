# 异常模型

单个 provider 失败时：

```java
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
        this.responseBody = responseBody;
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
}
```

全部 provider 都失败时：

```java
import java.util.List;

public class AllProvidersFailedException extends RuntimeException {

    private final List<LlmProviderException> failures;

    public AllProvidersFailedException(List<LlmProviderException> failures) {
        super("All LLM providers failed");
        this.failures = failures;
    }

    public List<LlmProviderException> failures() {
        return failures;
    }
}
```
