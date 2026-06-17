# SpringAiExceptionUtils

```java
package com.example.llm.client;

import org.springframework.web.client.RestClientResponseException;
import org.springframework.web.reactive.function.client.WebClientRequestException;
import org.springframework.web.reactive.function.client.WebClientResponseException;

/**
 * 从 Spring AI 包装异常中提取底层 HTTP 状态码、响应体和网络异常。
 */
public final class SpringAiExceptionUtils {

    private SpringAiExceptionUtils() {
    }

    public static Integer findHttpStatusCode(Throwable ex) {
        Throwable current = ex;

        while (current != null) {
            if (current instanceof WebClientResponseException webEx) {
                return webEx.getStatusCode().value();
            }

            if (current instanceof RestClientResponseException restEx) {
                return restEx.getRawStatusCode();
            }

            current = current.getCause();
        }

        return null;
    }

    public static String findResponseBody(Throwable ex) {
        Throwable current = ex;

        while (current != null) {
            if (current instanceof WebClientResponseException webEx) {
                return webEx.getResponseBodyAsString();
            }

            if (current instanceof RestClientResponseException restEx) {
                return restEx.getResponseBodyAsString();
            }

            current = current.getCause();
        }

        return "";
    }

    public static boolean isNetworkError(Throwable ex) {
        Throwable current = ex;

        while (current != null) {
            if (current instanceof WebClientRequestException) {
                return true;
            }

            current = current.getCause();
        }

        return false;
    }
}
```
