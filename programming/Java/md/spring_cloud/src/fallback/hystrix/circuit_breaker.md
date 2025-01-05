# 断路器

即使触发了降级逻辑, 但受限于 Hystrix 超时时间的问题, 频繁的调用依然很有可能产生堆积。

开启断路器后, 当调用失败达到一定程度后, 就不会再继续调用目标服务, 直接返回。一段时间后, 如果目标服务情况好转则恢复调用。

1. 修改 application.yml

```yaml
hystrix:
  command:
    default:
      metrics:
        rollingStats:
          # 时间窗口
          timeInMilliseconds: 10000
      circuitBreaker:
        # 失败率达到多少百分比后熔断
        errorThresholdPercentage: 50
        # 熔断触发的最小个数, 即在一定的时间窗口内请求达到一定的次数
        requestVolumeThreshold: 20
        # 熔断多长时间后, 尝试放一次请求进来
        sleepWindowInMilliseconds: 5000
```

10 秒内的 20 个请求中, 失败率达到 50% 的时候, 熔断器就会打开, 此时再调用此服务, 将会直接返回失败, 不再调远程服务。在熔断开启 5 秒后, 允许一次请求(即此时熔断为半开状态), 如果请求访问成功则关闭熔断, 恢复正常调用, 否则继续熔断 5 秒, 以此循环。
