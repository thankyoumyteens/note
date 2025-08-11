# 获取服务的真实 ip 地址

实现一个自定义的 feign 客户端(继承 feign.Client.Default)。

```java
@Slf4j
public class MyFeignClient extends Client.Default {

    public MyFeignClient(SSLSocketFactory sslContextFactory, HostnameVerifier hostnameVerifier) {
        super(sslContextFactory, hostnameVerifier);
    }

    @Override
    public Response execute(Request request, Request.Options options) throws IOException {
        try {
            return super.execute(request, options);
        } catch (IOException e) {
            // 打印服务的真实地址
            log.warn(" 请求 {} 异常 ======> {}", request.url(), e.getMessage());
            throw e;
        }
    }
}
```

用自定义客户端替换默认的 feign 客户端

```java
@Component
public class FeignConfig {

    public CachingSpringLoadBalancerFactory cachingLBClientFactory(SpringClientFactory factory) {
        return new CachingSpringLoadBalancerFactory(factory);
    }

    @Bean
    public Client feignClient(SpringClientFactory clientFactory) {
        CachingSpringLoadBalancerFactory bean = cachingLBClientFactory(clientFactory);
        return new LoadBalancerFeignClient(new MyFeignClient(null, null), bean, clientFactory);
    }
}
```
