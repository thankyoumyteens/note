# 监控平台如何监控 GC 日志

“监控平台如何监控 GC 日志”，其实可以拆成几层：

1. **GC 信息从哪儿来？（数据源）**
2. **怎么把 GC 信息送到监控平台？（采集方式）**
3. **监控平台拿到之后做什么？（展示 & 告警）**

在面试里，把这三层讲清楚，面试官会觉得你是「有做过完整链路」的人，而不是只会肉眼看 gc.log。

## 数据从哪儿来：GC 日志和 JVM 指标

常见有两种来源：

### 1. 传统 GC 日志文件（gc.log）

- 在 JVM 启动参数里配置：  
  JDK8 例如：

  ```bash
  -Xloggc:/path/to/logs/gc.log
  -XX:+PrintGCDetails
  -XX:+PrintGCDateStamps
  -XX:+PrintTenuringDistribution
  -XX:+PrintGCApplicationStoppedTime
  -XX:+PrintGCApplicationConcurrentTime
  ```

- 这样 GC 发生时，会把详情写入 gc.log，比如：
  - GC 类型（Young GC / Mixed GC / Full GC）
  - GC 前后堆大小，年轻代/老年代占用
  - STW（Stop-The-World）时间
  - 总耗时

### 2. 通过 JMX / Exporter 暴露 JVM 指标

现在更常见的方式是：**不直接扒日志文件，而是通过监控 Agent 将 GC 指标以监控指标的方式暴露出来**，比如：

- 使用 **Prometheus JMX Exporter**  
  在 JVM 启动时挂一个 javaagent：

  ```bash
  -javaagent:/path/jmx_prometheus_javaagent.jar=12345:/path/config.yml
  ```

- 通过 JMX 自动导出：
  - `jvm_gc_collection_seconds_count`
  - `jvm_gc_collection_seconds_sum`
  - Heap / Young / Old 区占用  
    等等

这样监控平台可以直接从 /metrics HTTP 接口拉指标，而不是解析文本日志。

## 怎么送到监控平台：采集方式

常见有两类思路

### 方案 A：基于日志系统采集 gc.log

适用于已经有 ELK / Loki / 自家日志平台的公司。

1. **应用输出 GC 日志到固定路径**  
   比如 `/var/log/appA/gc.log`。
2. **日志 Agent 采集**
   - 用 Filebeat / Logstash / Fluentd / 自研 Agent 等，配置一个采集规则：
     - 采集路径：`/var/log/appA/gc.log`
     - 指定编码和滚动策略
3. **在 Agent 侧或日志处理侧解析 GC 行**

   - 通过 Grok / 正则，把一行 GC 日志解析为结构化字段：

     比如：

     ```text
     2025-01-01T10:00:00.123+0800: 123.456: [GC pause (G1 Evacuation Pause) ... , 0.0456789 secs]
     ```

     解析出：

     - 时间：2025-01-01 10:00:00
     - GC 类型：G1 Evacuation Pause / Young / Mixed
     - STW 时间：45.6ms
     - GC 前后堆大小（可以选解析）

4. **写入监控平台**
   - 可以直接写入时序库（Prometheus/InfluxDB）作为 metrics，
   - 或者先入日志系统（ES/Loki），然后在监控平台上通过查询 + 聚合转换成指标。
5. **可视化 + 告警**
   - 在 Grafana / 自家监控页面做图表：
     - 每分钟 GC 次数
     - 每次 GC STW 时间
     - Young GC / Mixed GC 占比
     - 堆使用率曲线
   - 告警例子：
     - 5 分钟内 GC 总 STW 时间 > 2s
     - 某实例 10 分钟内发生 Mixed GC 次数 > N
     - Old 区使用率连续 5 分钟 > 80%

---

### 方案 B：基于 JVM / JMX / Agent 直接采集指标（推荐）

这是现在更主流也更优雅的方式，尤其是用了 Prometheus + Grafana 的团队。

1. **在应用 JVM 里挂监控 Agent**
   - JMX Exporter / SkyWalking Agent / Pinpoint / 自研 Agent 等
   - 这些 Agent 会定期通过 JMX 获取 JVM 内部指标，包括：
     - GC 次数、耗时
     - 各内存区域使用率
     - 线程数、类加载数等
2. **暴露 HTTP /metrics 接口**

   - 比如 Prometheus JMX Exporter 暴露：

     ```text
     jvm_gc_collection_seconds_count{gc="G1 Young Generation"} 1234
     jvm_gc_collection_seconds_sum{gc="G1 Young Generation"} 56.78
     ```

3. **监控平台拉取**
   - Prometheus 定期 `scrape` 应用的 /metrics
   - 或者其他监控系统通过 Agent 上报
4. **在监控平台上配置仪表盘和告警**
   - GC 相关的典型图表：
     - 各 GC 类型的次数 & 耗时累积曲线
     - 最近 5 分钟内单次 GC 平均耗时
     - 堆使用率 vs GC 频率
   - 告警策略同上。

**这一套的优点：**

- 不需要解析文本日志，结构化程度更高；
- 延迟低，常规是 15s ～ 1min 一次采集；
- 更容易和其他 JVM 指标结合起来看（堆、线程、CPU）。

## 回答时可以用的「半总结式」表述

如果在面试里，我会建议你这样组织答案（简化版，方便直接说）：

> 我理解的“监控平台监控 GC 日志”，其实分两种思路：
>
> 一类是传统的 **gc.log 日志采集 + 解析**，我们在 JVM 启动参数里打开 GC 日志输出，然后通过日志 Agent（比如 Filebeat/自研 Agent）把 gc.log 收集到日志平台，再用正则或 Grok 把单行 GC 日志解析成结构化字段，比如 GC 类型、耗时、堆前后大小等，最后在监控平台上做聚合图表和告警，比如 5 分钟内 GC 总耗时、Mixed GC 次数、Full GC 告警等。
>
> 另一类是现在更常用的 **JVM 指标采集**，直接通过 JMX Exporter 或监控 Agent，从 JVM 里拉取 GC 指标，比如各个 GC 的次数、总耗时、堆使用率这些，暴露为 /metrics 接口，由 Prometheus 之类的监控系统主动拉取。监控平台上就可以做 GC 频率 / STW 时间 / 堆使用率的趋势图，并根据阈值配置告警。
>
> 我个人更倾向于第二种方式，因为：
>
> 1. 不需要解析文本日志，数据更标准化；
> 2. 可以和其他 JVM 指标（堆、线程、CPU）放在同一张 Dashboard 上关联分析；
> 3. 告警阈值更容易统一配置，比如“5 分钟 GC 总 STW 时间超过 2s 就告警”。

如果你们公司现在有用哪套（比如 Prometheus + Grafana、ELK、自研监控），你再加一两句你们落地的具体做法，会非常加分。

## 那你们用 GC 监控主要是为了发现什么问题？看哪些指标？

- 重点关注：
  - GC 频率是否突然增高（可能有内存泄露或短期内大量对象创建）；
  - 单次 GC STW 时间是否变长（可能堆太大、老年代太满或 GC 配置不合理）；
  - Mixed GC / Full GC 是否频繁出现；
  - Old 区使用率是否长期高位。
- 有了这些监控之后，典型能发现：
  - 某次版本发布后，年轻代对象暴涨 → 分析是新功能里缓存 key 没有过期或集合无限增长；
  - 某服务在高峰期 Mixed GC 频繁 → 调整堆大小、G1 的 Region 配置，或者优化热点对象创建逻辑。
