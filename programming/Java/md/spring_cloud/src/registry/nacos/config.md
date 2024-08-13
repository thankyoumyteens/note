# 配置中心

Data ID 的命名规则: `${prefix}-${spring.profiles.active}.${file-extension}`。

- `prefix` 默认为 `spring.application.name` 的值，也可以通过配置项 `spring.cloud.nacos.config.prefix` 来配置
- `spring.profiles.active` 即为当前环境对应的 profile, 当 `spring.profiles.active` 为空时，对应的连接符 - 也将不存在，dataId 的拼接格式变成 `${prefix}.${file-extension}`
- `file-exetension` 为配置内容的数据格式，可以通过配置项 `spring.cloud.nacos.config.file-extension` 来配置。目前只支持 `properties` 和 `yaml` 类型

1. 添加依赖

```xml
<dependency>
    <groupId>com.alibaba.cloud</groupId>
    <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
    <version>2.2.9.RELEASE</version>
</dependency>
```

2. 注意是: bootstrap.yml

```yaml
server:
  port: 27442

spring:
  application:
    name: nacos-producer-demo
  cloud:
    nacos:
      discovery:
        server-addr: localhost:8848
      config:
        server-addr: localhost:8848
        file-extension: yml
```

3. 获取配置

```java
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.stereotype.Component;

@Component
// 实现配置的动态刷新
@RefreshScope
public class DemoConfigValue {

    @Value("${test}")
    private String test;

    public String getTest() {
        return test;
    }
}
```

4. 使用配置

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/producer")
public class ProducerController {

    @Autowired
    private DemoConfigValue demoConfigValue;

    @RequestMapping("/hello")
    public String hello() {
        return "hello" + demoConfigValue.getTest();
    }
}
```
