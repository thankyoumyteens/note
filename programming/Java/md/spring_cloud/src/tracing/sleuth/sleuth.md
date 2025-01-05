# Spring Cloud Sleuth

Spring Cloud Sleuth 只负责产生监控数据, 通过日志的方式展示出来, 并没有提供可视化的 UI 界面。

Spring Cloud 2022 版本开始, Spring Cloud Sleuth 项目被彻底移除, 项目的核心被移到了 Micrometer Tracing 项目中。

基本概念:

- Span：基本的工作单元, 相当于链表中的一个节点, 通过一个唯一 ID 标记它的开始、具体过程和结束。可以通过其中存储的开始和结束的时间戳来统计服务调用的耗时。除此之外还可以获取事件的名称、请求信息等
- Trace：一系列的 Span 串联形成的一个树状结构, 当请求到达系统的入口时就会创建一个唯一 ID(traceId), 唯一标识一条链路。这个 traceId 始终在服务之间传递, 直到请求的返回, 那么就可以使用这个 traceId 将整个请求串联起来, 形成一条完整的链路
- Annotation：用来标注微服务调用之间的事件:
  - cs(Client Send)：客户端发出请求, 开始一个请求的生命周期
  - sr(Server Received)：服务端接受请求并处理。`sr-cs = 网络延迟 = 服务调用的时间`
  - ss(Server Send)：服务端处理完毕准备发送到客户端。`ss - sr = 服务器上的请求处理时间`
  - cr(Client Reveived)：客户端接受到服务端的响应, 请求结束。`cr - sr = 请求的总时间`

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
2. traceId, 唯一标识一条链路
3. spanId, 链路中的基本工作单元 id
4. 表示是否将数据输出到其他服务, true 则会把信息输出到其他可视化的服务上观察
