# OpenFeign

2016 年，Netflix 将 Feign 捐献给社区，并改名为 OpenFeign。

1. 依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

OpenFeign 从 2.2.0.RELEASE 开始，增加了 Spring Cloud Loadbalancer 的依赖, 同时保留了 ribbon 的依赖。在 3.0.x，删除了 ribbon，只留下了 Loadbalancer。
