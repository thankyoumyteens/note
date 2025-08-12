# 获取微服务的真实 ip

## 方法 1

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
            // 也可以在这里打印服务的真实地址
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

## 方法 2

自定义 Feign 的 ErrorDecoder。这种方法只有当 Feign 调用失败时，才会在日志中打印出请求的 IP 地址。

```java
import feign.Response;
import feign.codec.ErrorDecoder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import javax.servlet.http.HttpServletRequest;

public class CustomErrorDecoder implements ErrorDecoder {
    private static final Logger logger = LoggerFactory.getLogger(CustomErrorDecoder.class);

    @Override
    public Exception decode(String methodKey, Response response) {
        // 通过RequestContextHolder获取HttpServletRequest
        HttpServletRequest request = ((ServletRequestAttributes) RequestContextHolder.getRequestAttributes()).getRequest();
        // 获取请求的IP地址
        String ip = request.getRemoteAddr();
        logger.error("Feign调用失败，请求IP: {}", ip);
        // 可以根据具体的响应状态码等信息返回不同的异常
        return new RuntimeException("Feign调用失败");
    }
}
```

配置 Feign 使用自定义的 ErrorDecoder

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class FeignConfig {

    @Bean
    public ErrorDecoder errorDecoder() {
        return new CustomErrorDecoder();
    }
}
```
