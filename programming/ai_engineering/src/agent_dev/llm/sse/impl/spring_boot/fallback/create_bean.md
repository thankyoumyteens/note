# 创建 Bean

```java
package com.example.llm.config;

import com.example.llm.dto.LlmProvider;
import com.example.llm.provider.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

/**
 * 创建 stream provider clients 和显式降级链。
 */
@Configuration
@EnableConfigurationProperties(LlmProperties.class)
public class LlmStreamProviderConfig {

    @Bean
    public LlmStreamProviderClient openAiResponsesStreamProviderClient(
            LlmProperties properties,
            ObjectMapper objectMapper
    ) {
        LlmProperties.ProviderProperties provider = properties.requiredProvider("openai-responses");

        return new OpenAiResponsesStreamProviderClient(
                "openai",
                provider.baseUrl(),
                "/responses",
                provider.apiKey(),
                provider.model(),
                60, // 60 秒内没有收到任何 SSE chunk，就认为上游 stream 卡死或断流。
                provider.maxRetriesOrDefault(),
                provider.connectTimeoutMillisOrDefault(),
                provider.responseTimeoutSecondsOrDefault(),
                objectMapper
        );
    }

    @Bean
    public LlmStreamProviderClient deepseekStreamProviderClient(
            LlmProperties properties,
            ObjectMapper objectMapper
    ) {
        LlmProperties.ProviderProperties provider = properties.requiredProvider("deepseek");

        return new OpenAiCompatibleStreamProviderClient(
                "deepseek",
                LlmProvider.DEEPSEEK,
                provider.baseUrl(),
                "/chat/completions",
                provider.apiKey(),
                provider.model(),
                60,
                provider.maxRetriesOrDefault(),
                provider.connectTimeoutMillisOrDefault(),
                provider.responseTimeoutSecondsOrDefault(),
                objectMapper
        );
    }

    @Bean
    public LlmStreamProviderClient anthropicStreamProviderClient(
            LlmProperties properties,
            ObjectMapper objectMapper
    ) {
        LlmProperties.ProviderProperties provider = properties.requiredProvider("anthropic");

        return new AnthropicStreamProviderClient(
                "anthropic",
                provider.baseUrl(),
                "/messages",
                provider.apiKey(),
                provider.model(),
                provider.anthropicVersion(),
                60,
                provider.maxRetriesOrDefault(),
                provider.connectTimeoutMillisOrDefault(),
                provider.responseTimeoutSecondsOrDefault(),
                objectMapper
        );
    }

    @Bean
    public StreamProviderFallbackRouter streamProviderFallbackRouter(
            List<LlmStreamProviderClient> clients,
            LlmProperties properties
    ) {
        Map<String, LlmStreamProviderClient> clientMap = clients.stream()
                .collect(Collectors.toMap(
                        LlmStreamProviderClient::provider,
                        Function.identity()
                ));

        List<LlmStreamProviderClient> orderedClients = properties.providerOrder()
                .stream()
                .map(providerName -> {
                    LlmStreamProviderClient client = clientMap.get(providerName);

                    if (client == null) {
                        throw new IllegalStateException("No stream provider client found: " + providerName);
                    }

                    return client;
                })
                .toList();

        return new StreamProviderFallbackRouter(orderedClients);
    }
}
```
