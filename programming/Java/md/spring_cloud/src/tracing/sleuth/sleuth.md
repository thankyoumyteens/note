# Spring Cloud Sleuth

Spring Cloud Sleuth 只负责产生监控数据，通过日志的方式展示出来，并没有提供可视化的 UI 界面。

Spring Cloud 2022 版本开始, Spring Cloud Sleuth 项目被彻底移除，项目的核心被移到了 Micrometer Tracing 项目中。

## 使用

1. 依赖

```xml
<dependency>
   <groupId>org.springframework.cloud</groupId>
   <artifactId>spring-cloud-starter-sleuth</artifactId>
</dependency>
```

2. 所有服务都需要调整日志级别

```yaml
logging:
  level:
    org.springframework.cloud.openfeign: debug
    org.springframework.cloud.sleuth: debug
```

3. 启动, 调用接口可以看到日志

```log
2024-09-14 17:12:43.140 DEBUG [gateway-demo,91969e315cb5c4fc,91969e315cb5c4fc,true] ...
```

日志格式中总共有四个部分:

1. 服务名称
2. traceId，唯一标识一条链路
3. spanId，链路中的基本工作单元 id
4. 表示是否将数据输出到其他服务，true 则会把信息输出到其他可视化的服务上观察
