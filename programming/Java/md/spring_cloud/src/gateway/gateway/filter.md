# 过滤器

## 添加请求头

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: myRoute1
          uri: https://example.org
          filters:
            - AddRequestHeader=X-Request-Foo, Bar
          predicates:
            - Path=/service1/**
```

## 重写路径

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: myRoute1
          uri: https://example.org
          filters:
            # 将/service1/(?.*)重写为{segment}, 然后转发到https://example.org
            # 比如请求localhost:8080/service1/page1, 会转发到https://example.org/page1
            - RewritePath=/service1/(?<segment>.*), /$\{segment}
          predicates:
            - Path=/service1/**
```

## 自定义过滤器

通过实现 GatewayFilter 和 Ordered 接口自定义 Filter

```java
import org.springframework.cloud.gateway.filter.GatewayFilter;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.core.Ordered;
import org.springframework.http.HttpCookie;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.stereotype.Component;
import org.springframework.util.MultiValueMap;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

import java.util.List;

@Component
public class MyFilter implements GatewayFilter, Ordered {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        MultiValueMap<String, HttpCookie> cookies = request.getCookies();
        List<HttpCookie> tokens = cookies.get("access_token");
        if (tokens == null || tokens.isEmpty()) {
            throw new RuntimeException("access_token is empty");
        }

        return chain.filter(exchange);
    }

    @Override
    public int getOrder() {
        // 给过滤器设定优先级
        // 值越大则优先级越低
        return 0;
    }
}
```

将过滤器注册到 router 中

```java
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;

@Bean
public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
    return builder.routes().route(r -> r.path("/service1/**")
            .filters(f -> f.filter(new MyFilter()))
            .uri("https://example.org")
            .id("route1")
    ).build();
}
```

## 自定义过滤器工厂

类名必须要以 GatewayFilterFactory 结尾

```java
import org.springframework.cloud.gateway.filter.GatewayFilter;
import org.springframework.cloud.gateway.filter.factory.AbstractGatewayFilterFactory;

import java.util.Arrays;
import java.util.List;

public class CheckAuthGatewayFilterFactory extends AbstractGatewayFilterFactory<CheckAuthGatewayFilterFactory.Config> {
    public CheckAuthGatewayFilterFactory() {
        super(Config.class);
    }

    @Override
    public List<String> shortcutFieldOrder() {
        return Arrays.asList("value");
    }

    @Override
    public GatewayFilter apply(Config config) {
        return (exchange, chain) -> {
            System.out.println("进入自定义过滤器, value：" + config.getValue());
            return chain.filter(exchange);
        };
    }

    // 用来接收配置文件中的参数
    public static class Config {
        private String value;

        public String getValue() {
            return value;
        }

        public void setValue(String value) {
            this.value = value;
        }
    }
}
```

交给 spring 管理

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class FilterConfig {
    @Bean
    public CheckAuthGatewayFilterFactory checkAuthGatewayFilterFactory() {
        return new CheckAuthGatewayFilterFactory();
    }
}
```

配置

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: myRoute1
          uri: lb://nacos-client-demo
          predicates:
            - Path=/test/**
          filters:
            - CheckAuth=myParam1
```

## 自定义全局过滤器

全局过滤器不必在路由上配置, 注入到 IOC 容器中即可全局生效

```java
@Component
@Order(value = Integer.MIN_VALUE)
public class AccessLogGlobalFilter implements GlobalFilter {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        // filter的前置处理
        ServerHttpRequest request = exchange.getRequest();
        String path = request.getPath().pathWithinApplication().value();
        InetSocketAddress remoteAddress = request.getRemoteAddress();
        return chain
               // 继续调用filter
               .filter(exchange)
               // filter的后置处理
               .then(Mono.fromRunnable(() -> {
                    ServerHttpResponse response = exchange.getResponse();
                    HttpStatus statusCode = response.getStatusCode();
                    log.info("请求路径:{},远程IP地址:{},响应码:{}", path, remoteAddress, statusCode);
               }));
    }
}
```
