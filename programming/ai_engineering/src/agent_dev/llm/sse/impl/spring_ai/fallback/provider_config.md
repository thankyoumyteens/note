# provider 配置

## application.yml

```yaml id="yd3a6x"
app:
  llm:
    provider-order:
      - openai
      - deepseek
      - anthropic

    providers:
      openai:
        base-url: https://api.openai.com
        completions-path: /v1/chat/completions
        api-key: ${OPENAI_API_KEY}
        model: gpt-4o-mini
        temperature: 0.2
        max-tokens: 1000
        stream-idle-timeout-seconds: 60
        request-timeout-seconds: 35
        max-retries: 2

      deepseek:
        base-url: https://api.deepseek.com
        completions-path: /chat/completions
        api-key: ${DEEPSEEK_API_KEY}
        model: deepseek-v4-pro
        temperature: 0.2
        max-tokens: 1000
        stream-idle-timeout-seconds: 60
        request-timeout-seconds: 35
        max-retries: 2

      anthropic:
        base-url: https://api.anthropic.com
        completions-path: /v1/messages
        api-key: ${ANTHROPIC_API_KEY}
        model: claude-sonnet-4-20250514
        temperature: 0.2
        max-tokens: 1000
        stream-idle-timeout-seconds: 60
        request-timeout-seconds: 35
        max-retries: 2
```

## LlmProperties

```java id="6p5mil"
package com.example.llm.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

import java.util.List;
import java.util.Map;

/**
 * LLM provider 配置。
 * providerOrder 决定 provider fallback 降级顺序。
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
            String completionsPath,
            String apiKey,
            String model,
            String anthropicVersion,
            Double temperature,
            Integer maxTokens,
            Integer requestTimeoutSeconds,
            Integer streamIdleTimeoutSeconds,
            Integer maxRetries
    ) {

        public double temperatureOrDefault() {
            return temperature == null ? 0.2 : temperature;
        }

        public int maxTokensOrDefault() {
            return maxTokens == null ? 1000 : maxTokens;
        }

        public int requestTimeoutSecondsOrDefault() {
            return requestTimeoutSeconds == null ? 35 : requestTimeoutSeconds;
        }

        public int streamIdleTimeoutSecondsOrDefault() {
            return streamIdleTimeoutSeconds == null ? 60 : streamIdleTimeoutSeconds;
        }

        public int maxRetriesOrDefault() {
            return maxRetries == null ? 2 : maxRetries;
        }
    }
}
```
