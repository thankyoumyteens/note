# 配置类

```java
package com.example.llm.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

import java.util.Map;

@ConfigurationProperties(prefix = "llm")
public record LlmProperties(
        String defaultProvider,
        Map<String, ProviderConfig> providers
) {
    public record ProviderConfig(
            String type,
            String baseUrl,
            String apiKey,
            String model
    ) {
    }
}
```

## 启动类上开启配置绑定

```java
package com.example;

import com.example.llm.config.LlmProperties;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

@SpringBootApplication
@EnableConfigurationProperties(LlmProperties.class)
public class AiDemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(AiDemoApplication.class, args);
    }
}
```
