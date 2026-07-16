# 创建 Bean

```java
package com.example.llm.config;

import com.example.llm.provider.AnthropicProviderClient;
import com.example.llm.provider.LlmProviderClient;
import com.example.llm.provider.OpenAiCompatibleProviderClient;
import com.example.llm.provider.ProviderFallbackRouter;
import com.example.llm.provider.OpenAiResponsesProviderClient;
import com.example.llm.recorder.LlmCallRecorder;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

/**
 * 统一创建 LLM provider client 和 provider fallback router。
 * Controller / Service 不直接 new ProviderClient。
 */
@Configuration
@EnableConfigurationProperties(LlmProperties.class)
public class LlmProviderConfig {

    // 输出 LLM 调用记录。
    private static final Logger log = LoggerFactory.getLogger(LlmProviderConfig.class);

    @Bean
    public LlmCallRecorder llmCallRecorder() {
        // 示例写日志；可替换为数据库实现。
        return record -> log.info("llmCall={}", record);
    }

    @Bean
    public LlmProviderClient openaiProviderClient(LlmProperties properties) {
        LlmProperties.ProviderProperties provider = properties.requiredProvider("openai");

        return new OpenAiResponsesProviderClient(
                "openai",
                provider.baseUrl(),
                provider.apiKey(),
                provider.model(),
                provider.requestTimeoutSecondsOrDefault(),
                provider.maxRetriesOrDefault(),
                provider.connectTimeoutMillisOrDefault(),
                provider.responseTimeoutSecondsOrDefault()
        );
    }
    @Bean
    public LlmProviderClient deepseekProviderClient(LlmProperties properties) {
        LlmProperties.ProviderProperties provider = properties.requiredProvider("deepseek");

        return new OpenAiCompatibleProviderClient(
                "deepseek",
                provider.baseUrl(),
                provider.apiKey(),
                provider.model(),
                provider.requestTimeoutSecondsOrDefault(),
                provider.maxRetriesOrDefault(),
                provider.connectTimeoutMillisOrDefault(),
                provider.responseTimeoutSecondsOrDefault()
        );
    }

    @Bean
    public LlmProviderClient anthropicProviderClient(LlmProperties properties) {
        LlmProperties.ProviderProperties provider = properties.requiredProvider("anthropic");

        return new AnthropicProviderClient(
                "anthropic",
                provider.baseUrl(),
                provider.apiKey(),
                provider.model(),
                provider.anthropicVersion(),
                provider.requestTimeoutSecondsOrDefault(),
                provider.maxRetriesOrDefault(),
                provider.connectTimeoutMillisOrDefault(),
                provider.responseTimeoutSecondsOrDefault()
        );
    }

    @Bean
    public ProviderFallbackRouter providerFallbackRouter(
            List<LlmProviderClient> clients,
            LlmProperties properties,
            LlmCallRecorder recorder
    ) {
        Map<String, LlmProviderClient> clientMap = clients.stream()
                .collect(Collectors.toMap(
                        LlmProviderClient::provider,
                        Function.identity()
                ));

        List<LlmProviderClient> orderedClients = properties.providerOrder()
                .stream()
                .map(providerName -> {
                    LlmProviderClient client = clientMap.get(providerName);

                    if (client == null) {
                        throw new IllegalStateException("No LlmProviderClient bean found: " + providerName);
                    }

                    return client;
                })
                .toList();

        return new ProviderFallbackRouter(orderedClients, recorder);
    }
}
```
