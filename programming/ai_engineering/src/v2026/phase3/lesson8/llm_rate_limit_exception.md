# 新增 LlmRateLimitException

AI Gateway 本地限流

新建：

```text
exception/LlmRateLimitException.java
```

```java
package com.example.aigateway.exception;

public class LlmRateLimitException extends RuntimeException {

    public LlmRateLimitException(String message) {
        super(message);
    }
}
```
