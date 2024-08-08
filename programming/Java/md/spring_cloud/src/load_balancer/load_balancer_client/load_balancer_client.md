# LoadBalancerClient

LoadBalancerClient 是 SpringCloud 提供的一种负载均衡客户端。

LoadBalancerClient 在初始化时会通过 Eureka Client 向 Eureka 服务端获取所有服务实例的注册信息并缓存在本地, 并且每 10 秒向 EurekaClient 发送 “ping”, 来判断服务的可用性。如果服务的可用性发生了改变或者服务数量和之前的不一致, 则更新或者重新拉取。最后, 在得到服务列表后, ILoadBalancer 会根据 IRule 的策略进行负载均衡（默认策略为轮询）。
