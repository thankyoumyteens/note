# provider 配置

下面的模型名是配置示例，运行时应替换为对应 Provider 当前可用的模型 ID。

## application.yml

```yaml
app:
  llm:
    # Provider 顺序配置
    # 不要在代码里硬编码降级顺序，建议从配置装配：
    provider-order:
      - openai
      - deepseek
      - anthropic

    providers:
      openai:
        base-url: https://api.openai.com/v1
        api-key: ${OPENAI_API_KEY}
        model: gpt-4o-mini
        connect-timeout-millis: 3000
        response-timeout-seconds: 30
        request-timeout-seconds: 35
        max-retries: 2

      deepseek:
        base-url: https://api.deepseek.com
        api-key: ${DEEPSEEK_API_KEY}
        model: deepseek-v4-pro
        connect-timeout-millis: 3000
        response-timeout-seconds: 30
        request-timeout-seconds: 35
        max-retries: 2

      anthropic:
        base-url: https://api.anthropic.com/v1
        api-key: ${ANTHROPIC_API_KEY}
        model: claude-haiku-4-5
        anthropic-version: 2023-06-01
        connect-timeout-millis: 3000
        response-timeout-seconds: 30
        request-timeout-seconds: 35
        max-retries: 2
```

## 配置对象：LlmProperties

```java
package com.example.llm.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

import java.util.List;
import java.util.Map;

/**
 * LLM provider 配置。
 * providerOrder 决定降级顺序，providers 保存每个 provider 的连接参数。
 */
@ConfigurationProperties(prefix = "app.llm")
public record LlmProperties(
        List<String> providerOrder,
        Map<String, ProviderProperties> providers
) {

    public LlmProperties {
        providerOrder = providerOrder == null ? List.of() : List.copyOf(providerOrder);
        providers = providers == null ? Map.of() : Map.copyOf(providers);
    }

    public ProviderProperties requiredProvider(String name) {
        ProviderProperties provider = providers.get(name);

        if (provider == null) {
            throw new IllegalStateException("Missing LLM provider config: " + name);
        }

        return provider;
    }

    public record ProviderProperties(
            String baseUrl,
            String apiKey,
            String model,
            String anthropicVersion,
            Integer connectTimeoutMillis,
            Integer responseTimeoutSeconds,
            Integer requestTimeoutSeconds,
            Integer maxRetries
    ) {

        public int connectTimeoutMillisOrDefault() {
            return connectTimeoutMillis == null ? 3000 : connectTimeoutMillis;
        }

        public int responseTimeoutSecondsOrDefault() {
            return responseTimeoutSeconds == null ? 30 : responseTimeoutSeconds;
        }

        public int requestTimeoutSecondsOrDefault() {
            return requestTimeoutSeconds == null ? 35 : requestTimeoutSeconds;
        }

        public int maxRetriesOrDefault() {
            return maxRetries == null ? 2 : maxRetries;
        }
    }
}
```
