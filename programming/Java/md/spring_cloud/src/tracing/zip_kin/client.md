# 客户端搭建

1. 依赖(由于 spring-cloud-starter-zipkin 中已经包含了 Spring Cloud Sleuth 依赖，因此只需要引入一个依赖即可)

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-zipkin</artifactId>
</dependency>
```

2. 配置文件(所有服务都需要配置)

```yaml
spring:
  cloud:
    sleuth:
      sampler:
        # 日志数据采样百分比，默认0.1(10%)，生产环境使用默认即可
        probability: 1.0
    zipkin:
      base-url: http://localhost:9411
      # 让nacos把它当成一个URL，而不要当做服务名
      discovery-client-enabled: false
```

3. 启动项目，并调用微服务的任意接口
4. 打开 http://localhost:9411, 进入"找到一个痕迹"页签, 点击 RUN QUERY 按钮可以看到刚才调用的接口, 点击 SHOW 进入详情查看服务调用的相关信息。进入"依赖"页签, 点击 RUN QUERY 按钮, 可以查看每个服务的依赖
