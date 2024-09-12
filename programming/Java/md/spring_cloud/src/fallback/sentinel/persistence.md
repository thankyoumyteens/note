# 限流规则持久化

Sentinel 默认限流规则是存储在内存中，只要服务重启之后对应得限流规则也会消失。

sentinel 提供了两种持久化模式:

- Pull 模式: 扩展写数据源（WritableDataSource）， 客户端主动向某个规则管理中心定期轮询拉取规则，这个规则中心可以是 RDBMS、文件 等
- Push 模式: 扩展读数据源（ReadableDataSource），规则中心统一推送，客户端通过注册监听器的方式时刻监听变化，即 Sentinel 控制台统一管理配置，然后将规则统一推送到 Nacos 并持久化，最后客户端监听 Nacos，下发配置生成 Rule。生产环境下一般采用 push 模式的数据源

## 客户端监听 Nacos

1. 依赖

```xml
<dependency>
    <groupId>com.alibaba.csp</groupId>
    <artifactId>sentinel-datasource-nacos</artifactId>
    <version>1.8.8</version>
</dependency>
```

2. bootstrap.yml

```yaml
spring:
  cloud:
    sentinel:
      transport:
        # 指定控制台的地址
        dashboard: localhost:8081
      # 取消控制台懒加载，项目启动即连接Sentinel
      eager: true
      datasource:
        # 配置流控规则持久化
        flow1:
          nacos:
            server-addr: localhost:8848
            # nacos配置的Data Id
            dataId: ${spring.application.name}-flow-rules
            # 配置文件的格式
            data-type: json
            # 规则类型: 流量控制
            rule-type: flow
```

3. 在 Nacos 创建文件 nacos-client-demo-flow-rules

```json
[
  {
    "resource": "demo",
    "limitApp": "default",
    "grade": 1,
    "count": 1,
    "clusterMode": false,
    "controlBehavior": 0,
    "strategy": 0,
    "warmUpPeriodSec": 10,
    "maxQueueingTimeMs": 500,
    "refResource": "rrr"
  }
]
```

4. 启动服务, 查看 Sentinel 控制台的流控规则是否已经获取到

## 修改 Sentinel 控制台

默认情况下 Sentinel 只能接收到 Nacos 推送的消息，但不能将自己控制台修改的信息同步给 Nacos, 要持久化规则就要在 nacos 中手动编写 json 文件。

如果要将 Sentinel 控制台修改的规则也同步到 Nacos，就需要修改 Sentinel 控制台的源码。

1. 下载源码: https://github.com/alibaba/Sentinel/archive/refs/tags/1.8.8.zip
