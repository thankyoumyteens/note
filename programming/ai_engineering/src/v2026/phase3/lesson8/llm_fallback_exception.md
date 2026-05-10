# 新增 LlmFallbackException

模型调用失败后触发 fallback

新建：

```text
exception/LlmFallbackException.java
```

```java
package com.example.aigateway.exception;

public class LlmFallbackException extends RuntimeException {

    public LlmFallbackException(String message, Throwable cause) {
        super(message, cause);
    }
}
```
