# 单个FeignClient接口开启日志

## 方法1

修改 application.yml 配置
```yaml
logging:
  level:
    # 要打印日志的接口
    com.example.demo.feign.FeignDemo: debug
# 下面的配置, 也可以写代码代替
# @Bean
# public Logger.Level level() { return Logger.Level.FULL; }
feign:
  client:
    config:
      default:
        loggerLevel: full

```

## 方法2

编写配置类
```java
@Configuration
public class FeignConfiguration {

    @Bean
    Logger.Level level() {
        return Logger.Level.FULL;
    }
}
```

在要打印日志的接口上添加`configuration = FeignConfiguration.class`
```java
@FeignClient(name = "demo", url = "https://www.baidu.com", configuration = FeignConfiguration.class)
public interface FeignDemo {
    @GetMapping("/")
    String test();
}
```

# 所有FeignClient接口开启日志

修改FeignConfiguration, 自定义feign.Logger
```java
@Configuration
public class FeignConfiguration {
    @Bean
    public feign.Logger logger() {
        return new Slf4jLogger();
    }
}
```

修改 application.yml 配置
```yaml
logging:
  level:
    # 删除具体的FeignClient接口配置, 只保留这一个就好了
    feign.Logger: debug
# 也可以写代码代替
# @Bean
# public Logger.Level level() { return Logger.Level.FULL; }
feign:
  client:
    config:
      default:
        loggerLevel: full
```
