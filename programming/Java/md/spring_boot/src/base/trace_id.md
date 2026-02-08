# 在日志中增加traceId用于链路追踪

在 Spring Boot 里，通过 `MDC（Mapped Diagnostic Context）+ 过滤器/拦截器` 的方式，把每次请求的 traceId 放到 MDC 里，然后在日志配置中使用 `%X{traceId}` 输出。这样同一次请求在不同日志里都会带上同一个 traceId，便于链路追踪。

### 1. 添加 TraceId 过滤器

注意：从 Spring Boot 3 开始，Servlet 相关包都从 `javax.servlet.*` 改成了 `jakarta.servlet.*`。

```java
package com.example.filter;

import org.slf4j.MDC;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.UUID;

public class TraceIdFilter implements Filter {

    public static final String TRACE_ID = "traceId";
    public static final String TRACE_HEADER = "X-Trace-Id";

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        // 每次 HTTP 请求进入时：
        // - 如果请求头里已经有 X-Trace-Id，就复用（方便链路透传）
        // - 否则自己生成一个
        String traceId = httpRequest.getHeader(TRACE_HEADER);
        if (traceId == null || traceId.isEmpty()) {
            traceId = generateTraceId();
        }

        // 把 traceId 放到 SLF4J 的 MDC 中
        MDC.put(TRACE_ID, traceId);

        // 响应头也带上 traceId，方便前端或调用方看到
        httpResponse.setHeader(TRACE_HEADER, traceId);

        try {
            chain.doFilter(request, response);
        } finally {
            // 请求结束后清理 MDC，避免线程复用导致串日志
            MDC.remove(TRACE_ID);
        }
    }

    private String generateTraceId() {
        // 可以根据自己需要自定义格式
        return UUID.randomUUID().toString().replace("-", "");
    }
}
```

### 2. 注册过滤器

```java
package com.example.config;

import com.example.filter.TraceIdFilter;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class WebConfig {

    @Bean
    public FilterRegistrationBean<TraceIdFilter> traceIdFilterRegistration() {
        FilterRegistrationBean<TraceIdFilter> registrationBean = new FilterRegistrationBean<>();
        registrationBean.setFilter(new TraceIdFilter());
        registrationBean.addUrlPatterns("/*"); // 所有路径都应用
        registrationBean.setOrder(1);          // 顺序靠前一点
        return registrationBean;
    }
}
```

### 3. 日志配置

最关键的是在 `pattern` 里加入 `%X{traceId}`。

配置文件放在 `src/main/resources/logback-spring.xml`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration scan="true" scanPeriod="60 seconds">

    <!-- 控制台输出 -->
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <!-- pattern 中加入 [%X{traceId}] -->
            <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level [%X{traceId}] %logger{36} - %msg%n</pattern>
            <charset>UTF-8</charset>
        </encoder>
    </appender>

    <!-- 根日志级别 -->
    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
    </root>

</configuration>
```

### 4. 示例 Controller

```java
package com.example.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/demo")
public class DemoController {

    private static final Logger log = LoggerFactory.getLogger(DemoController.class);

    @RequestMapping("/hello")
    public String hello() {
        log.info("业务处理完成，即将返回响应");
        return "Hello, World!";
    }
}
```
