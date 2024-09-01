# 集成 Feign

1. 依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
    <version>2.2.9.RELEASE</version>
</dependency>
```

2. 开启 sentinel

```yaml
feign:
  sentinel:
    enabled: true
```

3. fallback 类

```java
import org.springframework.stereotype.Component;

@Component
public class DemoFeignClientFallback implements DemoFeignClient {
    @Override
    public String hello() {
        return "fallback";
    }
}
```

4. 指定 fallback

```java
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.RequestMapping;

@FeignClient(name = "nacos-producer-demo", fallback = DemoFeignClientFallback.class)
public interface DemoFeignClient {

    @RequestMapping("/producer/hello")
    String hello();
}
```
