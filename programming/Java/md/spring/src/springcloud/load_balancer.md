# 负载均衡

spring-cloud 体系下的大多数产品都整合了 ribbon，如服务发现 nacos-discovery，RPC 调用 feign 组件等等，所以，使用时不用再引入 ribbon 依赖。

## Feign

feign 是 spring cloud 组件中的一个轻量级 restful 的 http 服务客户端，feign 通过封装包装请求体、发送 http 请求、获取接口响应结果、序列化响应结果等接口调用动作来简化接口的调用。

openfeign 则是在 feign 的基础上支持了 spring mvc 的注解，如@RequesMapping、@GetMapping、@PostMapping 等。openfeign 还实现与 Ribbon 的整合。

openfeign 通过包扫描将所有被 `@FeignClient` 注解注释的接口扫描出来，并为每个接口注册一个 FeignClientFactoryBean 实例。当 Spring 调用 FeignClientFactoryBean 的 getObject 方法时，openfeign 返回一个 Feign 生成的动态代理类，拦截方法的执行。

feign 会为代理的接口的每个方法都生成一个 MethodHandler。

当接口上的 `@FeignClient` 注解的 url 属性不配置时，就会走负载均衡逻辑，也就是需要与 Ribbon 整合使用。这时候会使用 LoadBalancerFeignClient 调用接口，由 LoadBalancerFeignClient 实现与 Ribbon 的整合。

## 常见的负载均衡算法

- 随机：通过随机选择服务进行执行，一般这种方式使用较少
- 轮询：请求来之后排队处理，轮着来
- 加权轮询：通过对服务器性能的分型，给高配置，低负载的服务器分配更高的权重，均衡各个服务器的压力
- 一致性 hash：通过客户端请求的地址的 hash 值取模映射进行服务器调度
- 最少并发：将请求分配到当前压力最小的服务器上

## 自定义 ribbon 的负载均衡策略

1. 实现 IRule 接口
2. 或者继承 AbstractLoadBalancerRule 类

## 配置自定义的负载均衡策略

1. 全局配置：当前服务调用其他微服务时，一律使用指定的负载均衡算法

```java
@Configuration
public class RibbonConfig {

    /**
     * 全局配置负载均衡策略
     */
    @Bean
    public IRule ribbonRule() {
        return new MyRule();
    }
}
```

2. 局部配置：当前服务调用指定的微服务时，才会使用对应的负载均衡算法

```yaml
# 被调用的微服务名
service1:
  ribbon:
    # 自定义的负载均衡策略
    NFLoadBalancerRuleClassName: com.demo.MyRule
```
