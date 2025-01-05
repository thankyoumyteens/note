# 配置刷新

配置文件修改后 Config Client 无法获取最新的值, 需要手动重启才会更新。

通过 actuator 实现手动刷新。通过 Spring Cloud Bus 实现自动刷新。

## 手动刷新, Config Client 修改

1. 增加 actuator 依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

2. application.yml 增加

```yaml
management:
  endpoints:
    web:
      exposure:
        # 开启 /actuator/refresh 接口
        include: refresh
```

3. controller 修改

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.context.config.annotation.RefreshScope;
import org.springframework.core.env.Environment;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/config")
// 通过@RefreshScope注解, 实现配置自动刷新
@RefreshScope
public class ConfigInfoController {
    @Autowired
    private Environment environment;

    @RequestMapping("/test")
    public String test() {
        return environment.getProperty("myKey");
    }
}
```

4. 修改配置后, POST 请求调用 http://localhost:27438/actuator/refresh 接口即可刷新配置
