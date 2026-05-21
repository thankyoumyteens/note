# 新增异常类

文件：

```text
src/main/java/com/example/aigateway/exception/AiStructuredOutputException.java
```

代码：

```java
package com.example.aigateway.exception;

/**
 * AI 结构化输出异常。
 *
 * 表示模型输出无法被解析为后端期望的结构化 DTO。
 *
 * 注意：
 * rawOutput 只用于服务端日志排查，不应该直接返回给外部用户。
 */
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
