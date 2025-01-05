# Spring Cloud Gateway

路由(Route)是 gateway 的基本模块。它由 ID、目标 URI、断言集合和过滤器集合组成。如果聚合断言结果为真, 则匹配到该路由。

- id: 区分不同的路由
- uri: 该路由转发的目标地址
- 断言(Predicate): 用于匹配请求, 如果为 true, 则执行路由
- 过滤器(Filter): 用于修改请求和响应的内容

```yaml
spring:
  cloud:
    gateway:
      # 定义路由
      routes:
        # 路由的id
        - id: myRoute1
          # 该路由转发的目标地址
          uri: http://target/path
          # 断言
          predicates:
            - Path=/orderInfo/**
          # 过滤器
          filters:
            # 将myKey=myVal添加到所有匹配请求的请求头中
            - AddRequestHeader=myKey, myVal
```
