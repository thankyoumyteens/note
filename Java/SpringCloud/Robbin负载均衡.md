# 负载均衡Robbin

首先我们启动两个user-service实例, 一个8081, 一个8082。


## 开启负载均衡

因为Eureka中已经集成了Ribbon, 所以我们无需引入新的依赖。直接修改代码: 

在RestTemplate的配置方法上添加`@LoadBalanced`注解: 
```java
@Bean
@LoadBalanced
public RestTemplate restTemplate() {
    return new RestTemplate(new OkHttp3ClientHttpRequestFactory());
}
```

修改调用方式, 不再手动获取ip和端口, 而是直接通过服务名称调用: 
```java
@Service
public class UserService {

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private DiscoveryClient discoveryClient;

    public List<User> queryUserByIds(List<Long> ids) {
        List<User> users = new ArrayList<>();
        // 地址直接写服务名称即可
        String baseUrl = "http://user-service/user/";
        ids.forEach(id -> {
            // 我们测试多次查询, 
            users.add(this.restTemplate.getForObject(baseUrl + id, User.class));
            // 每次间隔500毫秒
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });
        return users;
    }
}
```

## 负载均衡策略

Ribbon默认的负载均衡策略是简单的轮询

SpringBoot帮我们提供了修改负载均衡规则的配置入口: 

```yaml
user-service:
  ribbon:
    NFLoadBalancerRuleClassName: com.netflix.loadbalancer.RandomRule
```

格式是: `{服务名称}.ribbon.NFLoadBalancerRuleClassName`, 值就是IRule的实现类。

再次测试, 发现结果变成了随机

## 重试机制

Eureka的服务治理强调了CAP原则中的AP, 即可用性和可靠性。它与Zookeeper这一类强调CP(一致性, 可靠性)的服务治理框架最大的区别在于: Eureka为了实现更高的服务可用性, 牺牲了一定的一致性, 极端情况下它宁愿接收故障实例也不愿丢掉健康实例, 正如我们上面所说的自我保护机制。

但是, 此时如果我们调用了这些不正常的服务, 调用就会失败, 从而导致其它服务不能正常工作！这显然不是我们愿意看到的。

Spring Cloud 整合了Spring Retry 来增强RestTemplate的重试能力, 当一次服务调用失败后, 不会立即抛出一次, 而是再次重试另一个服务。

只需要简单配置即可实现Ribbon的重试: 

```yaml
spring:
  cloud:
    loadbalancer:
      retry:
        enabled: true # 开启Spring Cloud的重试功能
user-service:
  ribbon:
    ConnectTimeout: 250 # Ribbon的连接超时时间
    ReadTimeout: 1000 # Ribbon的数据读取超时时间
    OkToRetryOnAllOperations: true # 是否对所有操作都进行重试
    MaxAutoRetriesNextServer: 1 # 切换实例的重试次数
    MaxAutoRetries: 1 # 对当前实例的重试次数
```

根据如上配置, 当访问到某个服务超时后, 它会再次尝试访问下一个服务实例, 如果不行就再换一个实例, 如果不行, 则返回失败。切换次数取决于`MaxAutoRetriesNextServer`参数的值

引入spring-retry依赖

```xml
<dependency>
    <groupId>org.springframework.retry</groupId>
    <artifactId>spring-retry</artifactId>
</dependency>
```
