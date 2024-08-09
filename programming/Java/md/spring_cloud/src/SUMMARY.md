# Summary

- [Spring Cloud](./spring_cloud.md)
  - [父项目搭建](./project.md)

- [注册中心](./registry/registry.md)
  - [Eureka](./registry/eureka/eureka.md)
    - [创建注册中心](./registry/eureka/eureka_server.md)
    - [创建服务提供方](./registry/eureka/eureka_client.md)
    - [服务发现](./registry/eureka/eureka_discovery.md)
  - [Consul](./registry/consul/consul.md)
    - [安装](./registry/consul/install.md)
    - [创建服务提供方](./registry/consul/consul_client.md)
    - [服务发现](./registry/consul/consul_discovery.md)

- [负载均衡](./load_balancer/load_balancer.md)
  - [LoadBalancerClient](./load_balancer/load_balancer_client/load_balancer_client.md)
  - [Ribbon](./load_balancer/load_balancer_client/ribbon_client.md)

- [服务调用](./http_clients/http_clients.md)
  - [Feign](./http_clients/feign/feign.md)

- [配置中心](./config/config.md)
  - [Spring Cloud Config](./config/spring_config/spring_config.md)
    - [Config Server](./config/spring_config/config_server.md)
    - [获取配置](./config/spring_config/config_client.md)
    - [高可用](./config/spring_config/ha.md)
    - [配置刷新](./config/spring_config/refresh.md)

- [服务降级](./fallback/fallback.md)
  - [Hystrix](./fallback/hystrix/hystrix.md)
    - [服务降级](./fallback/hystrix/fallback.md)
    - [线程隔离](./fallback/hystrix/thread_isolation.md)
    - [断路器](./fallback/hystrix/circuit_breaker.md)
    - [集成Feign](./fallback/hystrix/feign.md)

- [网关](./gateway/gateway.md)
