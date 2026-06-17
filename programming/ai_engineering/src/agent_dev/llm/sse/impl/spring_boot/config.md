# 配置属性类

```java
package com.example.ai.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

import java.util.Map;

/**
 * 多 provider 配置。
 * provider 的协议类型、base-url、模型名、token 限制都从 application.yml 读取。
 */
@ConfigurationProperties(prefix = "app.ai")
public record AiProviderProperties(
        Map<String, ProviderConfig> providers
) {

    public ProviderConfig getRequiredProvider(String name) {
        ProviderConfig config = providers.get(name);
        if (config == null) {
            throw new IllegalArgumentException("Unknown provider: " + name);
        }
        return config;
    }

    public record ProviderConfig(
            ProviderType type,
            String apiKey,
            String baseUrl,
            String path,
            String model,
            Double temperature,
            Integer maxTokens,
            Boolean thinkingDisabled
    ) {
    }

    public enum ProviderType {
        OPENAI_CHAT_COMPLETIONS,
        ANTHROPIC_MESSAGES
    }
}
```

## 启动类

```java
package com.example;

import com.example.ai.config.AiProviderProperties;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

@EnableConfigurationProperties(AiProviderProperties.class)
@SpringBootApplication
public class AgentDevApplication {

    public static void main(String[] args) {
        SpringApplication.run(AgentDevApplication.class, args);
    }
}
```
