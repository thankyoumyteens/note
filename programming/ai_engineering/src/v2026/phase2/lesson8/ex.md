# 新增异常

## 新增限流异常

文件：

```text
src/main/java/com/example/aigateway/exception/LlmRateLimitException.java
```

```java
package com.example.aigateway.exception;

/**
 * AI Gateway 本地限流异常。
 */
public class LlmRateLimitException extends RuntimeException {

    public LlmRateLimitException(String message) {
        super(message);
    }
}
```

---

## 新增 fallback 异常

文件：

```text
src/main/java/com/example/aigateway/exception/LlmFallbackException.java
```

```java
package com.example.aigateway.exception;

/**
 * 模型调用失败后的 fallback 异常。
 */
public class LlmFallbackException extends RuntimeException {

    public LlmFallbackException(String message, Throwable cause) {
        super(message, cause);
    }
}
```
