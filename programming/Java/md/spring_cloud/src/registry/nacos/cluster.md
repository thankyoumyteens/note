# 服务分级存储模型

Nacos 服务分级存储模型：一级是服务, 二级是集群(比如按区域机房划分: 北京集群, 上海集群等), 三级是实例(同一集群内的多个服务提供者实例)。在服务互相调用时应该尽可能地去选择本地集群，即同一集群的服务，因为跨集群调用延迟较高，只有当本地集群的需调用的服务不可访问时，再去访问其它集群。

## 配置集群

在 nacos 注册的服务如果没有配置集群的话，默认是没有集群的，也就是在一个名为 DEFAULT 的集群下。

可以在配置文件中指定该服务的集群:

```yaml
spring:
  application:
    name: service1
  cloud:
    nacos:
      server-addr: http://localhost:8848
      discovery:
        # 配置集群名称
        cluster-name: BJ
```

## 配置优先访问同一集群

nacos 默认的负载均衡策略是轮询，也就是会轮询各个服务，不会区别是否同一集群。

### Ribbon 的配置

Nacos 中提供了一个 NacosRule 的实现，可以优先从同集群中挑选实例:

```yaml
# 要调用的服务名
service2:
  ribbon:
    # 负载均衡规则(优先访问同一集群下的微服务，是随机访问，而不是轮询)
    NFLoadBalancerRuleClassName: com.alibaba.cloud.nacos.ribbon.NacosRule
```

### Spring Cloud Loadbalancer 的配置

```yaml
spring:
  cloud:
    loadbalancer:
      nacos:
        enabled: true
```

## 配置实例的权重

当配置了优先访问同一集群内的服务时，在同一集群内如果有多个服务提供者实例的话，此时会使用随机访问的策略。

Nacos 也提供了权重配置来控制实例的访问频率，权重越大则访问频率越高。

可以在 Nacos 的控制台中设置实例的权重值。所有的实例的权重值默认都是 1，可以将将权重值设置为 0~1，权重越低，被访问到的概率就越低，为 0 时则完全不会被访问到。
