# 加载配置文件

日常项目开发中，经常遇到使用多级配置的情况，springboot 中可以使用 @ConfigurationProperties 来加载。

yml 文件内容:

```yaml
my-props:
  my-config1: hello
  my-config2:
    target-path: /temp
```

加载 yml 配置:

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

import lombok.Data;

@Data
@Configuration
@ConfigurationProperties("my-props")
public class YlConf{

    private String myConfig1;

    @Autowired
    private MyConfig2 myConfig2;

    @Data
    @Configuration
    @ConfigurationProperties("my-props.my-config2")
    public class MyConfig2{
        private String targetPath;
    }
}
```
