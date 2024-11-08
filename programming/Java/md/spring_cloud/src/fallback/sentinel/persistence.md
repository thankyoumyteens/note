# 限流规则持久化

Sentinel 默认限流规则是存储在内存中，只要服务重启之后对应得限流规则也会消失。

sentinel 提供了两种持久化模式:

- Pull 模式: 扩展写数据源(WritableDataSource)， 客户端主动向某个规则管理中心定期轮询拉取规则，这个规则中心可以是 RDBMS、文件 等
- Push 模式: 扩展读数据源(ReadableDataSource)，规则中心统一推送，客户端通过注册监听器的方式时刻监听变化，即 Sentinel 控制台统一管理配置，然后将规则统一推送到 Nacos 并持久化，最后客户端监听 Nacos，下发配置生成 Rule。生产环境下一般采用 push 模式的数据源

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

## 规则 json

### 流控规则

```json
[
  {
    // 资源名
    "resource": "",
    // 针对来源
    "limitApp": "default",
    // 阈值类型 1:QPS 0:并发线程数
    "grade": 1,
    // 单机阈值
    "count": 1,
    // 是否集群
    "clusterMode": false,
    // 集群配置
    "clusterConfig": {
      // 全局唯一的规则 ID，由集群限流管控端分配
      "flowId": 1,
      // 阈值模式 0: 单机均摊 1:总体阈值
      "thresholdType": 1,
      // 在 client 连接失败或通信失败时，是否退化到本地的限流模式
      "fallbackToLocalWhenFail": true,
      // 流控模式 0:直接 1:关联 2:链路
      "strategy": 0,
      // 滑动窗口时间，默认1s
      "windowIntervalMs": 1000
    },
    // 流控模式 0:直接 1:关联 2:链路
    "strategy": 0,
    // 流控效果 0:流控效果 1:Warm Up 2:排队等待
    "controlBehavior": 0,
    // 预热时长 秒 预热模式需要此参数
    "warmUpPeriodSec": 10,
    // 超时时间 毫秒 排队等待模式需要此参数
    "maxQueueingTimeMs": 500,
    // 关联资源/入口资源 关联/链路模式需要此参数
    "refResource": ""
  }
]
```

### 熔断规则

```json
[
  {
    // 资源名
    "resource": "",
    // 熔断策略 0:慢调用比例 1:异常比例 2:异常数
    "grade": 0,
    // 最大 RT/比例阈值/异常数
    "count": 200,
    // 慢调用比例阈值，仅慢调用比例模式有效
    "slowRatioThreshold": 0.2,
    // 最小请求数
    "minRequestAmount": 5,
    // 统计时长
    "statIntervalMs": 1000,
    // 熔断时长
    "timeWindow": 10
  }
]
```

### 热点规则

```json
[
  {
    // 资源名
    "resource": "",
    // 限流模式 QPS 模式，不可更改
    "grade": 1,
    // 参数索引
    "paramIdx": 0,
    // 单机阈值
    "count": 13,
    // 统计窗口时长
    "durationInSec": 6,
    // 是否集群 默认false
    "clusterMode": false,
    // 集群配置
    "clusterConfig": {
      // 全局唯一的规则 ID，由集群限流管控端分配
      "flowId": 1,
      // 阈值模式 0: 单机均摊 1:总体阈值
      "thresholdType": 1,
      // 在 client 连接失败或通信失败时，是否退化到本地的限流模式
      "fallbackToLocalWhenFail": true,
      // 流控模式 0:直接 1:关联 2:链路
      "strategy": 0,
      // 滑动窗口时间，默认1s
      "windowIntervalMs": 1000
    },
    // 参数例外项
    "paramFlowItemList": [
      {
        // 参数类型
        "classType": "int",
        // 限流阈值
        "count": 1,
        // 参数值
        "object": "1"
      }
    ]
  }
]
```

### 系统规则

```json
[
  {
    // RT
    "avgRt": 1,
    // CPU 使用率
    "highestCpuUsage": -1,
    // LOAD
    "highestSystemLoad": -1,
    // 线程数
    "maxThread": -1,
    // 入口 QPS
    "qps": -1
  }
]
```

### 授权规则

```json
[
  {
    // 资源名
    "resource": "",
    // 流控应用
    "limitApp": "",
    // 授权类型 0:白名单 1:代表黑名单
    "strategy": 0
  }
]
```

## 修改 Sentinel 控制台

默认情况下 Sentinel 只能接收到 Nacos 推送的消息，但不能将自己控制台修改的信息同步给 Nacos, 要持久化规则就要在 nacos 中手动编写 json 文件。

如果要将 Sentinel 控制台修改的规则也同步到 Nacos，就需要修改 Sentinel 控制台的源码。

1. 下载源码: https://github.com/alibaba/Sentinel/archive/refs/tags/1.8.8.zip

todo
