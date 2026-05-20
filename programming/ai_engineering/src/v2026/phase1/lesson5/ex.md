# 新增异常类

新建包：

```text
exception
```

新建文件：

```text
exception/AiStructuredOutputException.java
```

代码：

```java
package com.example.aigateway.exception;

public class AiStructuredOutputException extends RuntimeException {

    private final String rawOutput;

    public AiStructuredOutputException(String message, String rawOutput, Throwable cause) {
        super(message, cause);
        this.rawOutput = rawOutput;
    }

    public String getRawOutput() {
        return rawOutput;
    }
}
```
