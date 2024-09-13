# 断言

Predicate 来自于 java8 的接口。Predicate 接受一个输入参数，返回一个布尔值结果。在 Gateway 中，有一些的内置 Predicate Factory，在运行时，Gateway 会自动根据需要创建对应的 Pridicate 对象。

## Path

根据请求路径匹配路由

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: path_route
          uri: https://example.org
          predicates:
            # 每个路径模式以逗号分开
            - Path=/service1/**,/service2/**
```

## After

在指定日期时间之后收到的请求都将被匹配

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: after_route
          uri: https://example.org
          predicates:
            # UTC时间格式
            - After=2018-03-18T17:32:58.129+08:00[Asia/Shanghai]
```

## Before

在指定日期时间之前收到的请求都将被匹配

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: before_route
          uri: https://example.org
          predicates:
            # UTC时间格式
            - Before=2018-03-18T17:32:58.129+08:00[Asia/Shanghai]
```

## Cookie

cookie 存在指定名称，并且对应的值符合指定正则表达式，则匹配成功

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: cookie_route
          uri: https://example.org
          predicates:
            # 名称 cookie的名称
            # val1 cookie值的正则表达式
            - Cookie=key1, val1
```

## Header

请求头中存在指定名称，并且对应的值符合指定正则表达式，则匹配成功

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: header_route
          uri: https://example.org
          predicates:
            - Header=X-Request-Id, \d+
```

## Host

请求的 host 要和指定的正则表达式匹配

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: host_route
          uri: https://example.org
          predicates:
            - Host=**.demo1.com:8081,**.demo2.com
```

## Method

匹配指定的请求方法类型

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: method_route
          uri: https://example.org
          predicates:
            - Method=GET,POST
```

## RemoteAddr

匹配指定来源的请求

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: remoteaddr_route
          uri: https://example.org
          predicates:
            # 192.168.1.100是IP地址, 24是子网掩码
            - RemoteAddr=192.168.1.100/24
```

## Query

匹配请求中是否带有指定的参数

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: query_route
          uri: https://example.org
          predicates:
            - Query=myParam1,\d
```
