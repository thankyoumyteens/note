# 集群

Eureka Server 除了单点运行之外, 还可以通过运行多个实例, 并进行互相注册的方式来实现高可用的部署, 所以只需要将当前节点注册到其它可用的 serviceUrl 就能实现高可用部署。

1. application.yml

```yaml
eureka:
  client:
    # 服务注册中心的地址
    serviceUrl:
      defaultZone: http://其它EurekaServer的地址/eureka/
```
