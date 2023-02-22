# FeignClient注解

FeignClient注解的作用目标在接口上

# 常用属性

- name/value 指定FeignClient的名称，如果项目是微服务，name属性指定的是调用服务的微服务名称
- url 指定调用服务的全路径, 经常用于本地测试, 如果同时指定name和url属性, 则以url属性为准,name属性指定的值便当做客户端的名称
- decode404 当发生http 404错误时，如果该字段为true，会调用decoder进行解码，否则抛出FeignException
- configuration 指定Feign配置类，可以自定义Feign的Encoder、Decoder、LogLevel、Contract
- fallback 当调用远程接口失败或超时时，会调用对应接口的容错逻辑，fallback指定的类必须实现@FeignClient标记的接口
- fallbackFactory 用于生成fallback类实例，通过这个属性我们可以实现每个接口通用的容错逻辑，减少重复的代码
- path 定义当前FeignClient的统一前缀

# 使用FeignClient

依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
    <version>2.0.2.RELEASE</version>
</dependency>
<dependency>
    <groupId>io.github.openfeign</groupId>
    <artifactId>feign-core</artifactId>
    <version>9.7.0</version>
</dependency>
<dependency>
    <groupId>io.github.openfeign</groupId>
    <artifactId>feign-slf4j</artifactId>
    <version>9.7.0</version>
</dependency>
```

添加FeignClients启用注解

```java
@SpringBootApplication
@EnableFeignClients
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

FeignClient代码

```java
@FeignClient(name = "myFeignClient", url = "http://127.0.0.1:8001")
public interface MyFeignClient {
    @RequestMapping(method = RequestMethod.GET, value = "/participate")
    String getCategorys(@RequestParam Map<String, Object> params);
}
```

调用

```java
@Autowired
MyFeignClient myFeignClient;

String r = myFeignClient.getCategorys();
```
