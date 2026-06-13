# 配置属性类

```java
package com.example.ai.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

import java.util.Map;

@ConfigurationProperties(prefix = "app.ai")
public record AiProviderProperties(
        String defaultProvider,
        Map<String, ProviderConfig> providers
) {

    public record ProviderConfig(
            String apiKey,
            String baseUrl,
            String completionsPath,
            String version,
            String model,
            Double temperature,
            Integer maxTokens
    ) {
    }

    public ProviderConfig getRequiredProvider(String name) {
        ProviderConfig provider = providers.get(name);
        if (provider == null) {
            throw new IllegalStateException("Missing AI provider config: " + name);
        }
        return provider;
    }
}
```

启动类上加：

```java
package com.example;

import com.example.ai.config.AiProviderProperties;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

@EnableConfigurationProperties(AiProviderProperties.class)
@SpringBootApplication
public class DemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```
