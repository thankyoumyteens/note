# Spring Cloud Gateway

路由(Route)的组成:

- id
- 目标 URI: 该路由转发的目标地址
- 断言: 用于匹配请求, 如果为 true, 则执行路由
- 过滤器: 用于修改请求和响应

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
