# 自定义限流异常信息

三种方式:

- 通过配置文件指定返回内容
- 通过配置文件重定向到指定地址
- 代码中自定义响应内容

## 配置文件

1. 配置

```yaml
server:
  port: 8090

spring:
  application:
    name: gateway-demo
  cloud:
    nacos:
      discovery:
        server-addr: localhost:8848
    sentinel:
      transport:
        dashboard: localhost:8081
      eager: true
      # 限流后的响应内容
      scg:
        fallback:
          mode: response
          # HTTP状态码
          response-status: 200
          # 响应体
          response-body: '{"message": "限流"}'
    gateway:
      routes:
        - id: myRoute1
          uri: lb://nacos-client-demo
          predicates:
            - Path=/test/**
```

## 重定向到指定地址

```yaml
server:
  port: 8090

spring:
  application:
    name: gateway-demo
  cloud:
    nacos:
      discovery:
        server-addr: localhost:8848
    sentinel:
      transport:
        dashboard: localhost:8081
      eager: true
      # 限流后的响应内容
      scg:
        fallback:
          mode: redirect
          redirect: http://localhost/fallback
    gateway:
      routes:
        - id: myRoute1
          uri: lb://nacos-client-demo
          predicates:
            - Path=/test/**
```

## 代码中指定

1. 实现 BlockRequestHandler

```java
import com.alibaba.csp.sentinel.adapter.gateway.sc.callback.BlockRequestHandler;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.server.ServerResponse;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

public class SentinelFallbackHandler implements BlockRequestHandler {

    @Override
    public Mono<ServerResponse> handleRequest(ServerWebExchange serverWebExchange, Throwable throwable) {
        return ServerResponse.status(200).contentType(MediaType.APPLICATION_JSON).bodyValue("{\"message\":\"限流\"}");
    }
}
```

2. 添加到 spring

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.annotation.Order;

@Configuration
public class GatewayConfig {

    @Bean
    @Order(-1)
    public SentinelFallbackHandler sentinelFallbackHandler() {
        return new SentinelFallbackHandler();
    }
}
```
