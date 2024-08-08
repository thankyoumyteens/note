# 限流

为什么要限流:

- 并发量大
- 防止恶意刷接口

限流的实现方式: 

- tomcat 设置最大连接数
- nginx 限流
- 网关限流
- 自定义拦截器

## nginx 限流

两种方式

1. 配置速率
2. 控制并发连接数

### 配置速率

配置速率限制需要使用两个主要指令, limit_req_zone 和 limit_req

```conf
# 定义速率限制
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s;

server {
    location /login/ {
        # 启用速率限制
        limit_req zone=mylimit;

        proxy_pass http://my_upstream;
    }
}
```

limit_req_zone 指令用于定义速率限制的参数。

limit_req 在其出现的上下文环境中启用速率限制（比如指向 `/login/` 的所有请求）。

limit_req_zone 指令通常在 http 模块中定义, 以便其可用于多个上下文。limit_req_zone 指令后面有三个部分: 

- 限流对象。比如 nginx 变量 `$binary_remote_addr`, 表示对每个客户端 IP 地址进行限制
- zone – 定义共享内存区域来存储访问信息。将信息保存在共享内存中意味着可以在 NGINX worker 进程之间共享该信息。mylimit 是自定义的 zone 的名称。10m 可以存储约 160,000 个 ip 地址的访问信息
- rate – 最大访问速率。`10r/s` 表示速率不能超过每秒 10 个请求。nginx 实际上以毫秒粒度跟踪请求, 因此这个配置实际是每 100 毫秒 1 个请求。如果请求在上一个允许的请求之后不到 100 毫秒到达, 则该请求将被拒绝

### 控制并发连接数

```conf
# 定义并发连接数限制
limit_conn_zone $binary_remote_addr zone=mylimit1:10m;
limit_conn_zone $server_name zone=mylimit2:10m;

server {
    location /login/ {
        # 表示单个ip同时最多能持有20个连接
        limit_conn mylimit1 20;
        # 表示虚拟主机同时最多能处理100个连接
        limit_conn mylimit2 100;

        proxy_pass http://my_upstream;
    }
}
```

## 网关限流

Spring Cloud Gateway 是 Spring Cloud 推出的第二代网关框架, 取代 Zuul 网关。

Spring Cloud Gateway 自带了限流方案, 依赖 redis 与内置的 RedisRateLimiter 过滤器进行限流操作, 默认限流算法为令牌桶算法。

1. 引入 redis 依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis-reactive</artifactId>
</dependency>
```

2. 配置 redis

```yaml
redis:
  host: 127.0.0.1
  port: 6379
```

3. 注入 KeyResolver

```java
@Configuration
public class GatewayResolver {
  @Bean("myKeyResolver")
  public KeyResolver hostAddrKeyResolver() {
    return exchange -> {
      // 根据url限流
      String url = exchange.getRequest().getPath().toString();
      return Mono.just(url);
    };
  }
}
```

4. 配置文件

```yaml
spring:
  cloud:
    gateway:
      - id: test
        uri: http://httpbin.org:80/get
        filters:
          - name: RequestRateLimiter
            args:
              key-resolver: "#{@myKeyResolver}"
              # 令牌桶恢复速度, 即每秒访问个数
              redis-rate-limiter.replenishRate: 1
              # 令牌桶大小, 即峰值流量来临时最大可访问数
              redis-rate-limiter.burstCapacity: 3
```
