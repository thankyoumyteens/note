# 集成 Feign

1. hystrix 依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
    <version>2.2.10.RELEASE</version>
</dependency>
```

2. application.yml 开启 hystrix

```yaml
feign:
  hystrix:
    enabled: true
```

3. 启动类开启断路器功能

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.netflix.hystrix.EnableHystrix;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
// 开启服务发现功能
@EnableDiscoveryClient
// 开启Feign功能
@EnableFeignClients
// 开启断路器功能
@EnableHystrix
public class FeignDemo {
    public static void main(String[] args) {
        SpringApplication.run(FeignDemo.class, args);
    }
}
```

4. 定义降级方法

```java
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Component
public class DemoFeignClientFallback implements DemoFeignClient {
    @Override
    public List<String> getServiceList() {
        return new ArrayList<>();
    }
}
```

5. FeignClient 指定降级方法

```java
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

// 指定服务名和降级方法
@FeignClient(name = "eureka-client-demo", fallback = DemoFeignClientFallback.class)
public interface DemoFeignClient {

    @RequestMapping("/service/list")
    List<String> getServiceList();
}
```
