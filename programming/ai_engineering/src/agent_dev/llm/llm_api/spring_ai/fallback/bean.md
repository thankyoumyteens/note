# 创建 Bean

这里创建：

```text
OpenAI ChatClient
DeepSeek ChatClient
Anthropic ChatClient
ProviderClient
ProviderFallbackRouter
```

```java
package com.example.llm.config;

import com.example.llm.client.LlmProviderClient;
import com.example.llm.client.SpringAiProviderClient;
import com.example.llm.dto.LlmProvider;
import com.example.llm.router.ProviderFallbackRouter;
import io.micrometer.observation.ObservationRegistry;
import org.springframework.ai.anthropic.AnthropicChatModel;
import org.springframework.ai.anthropic.AnthropicChatOptions;
import org.springframework.ai.anthropic.api.AnthropicApi;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.model.tool.ToolCallingManager;
import org.springframework.ai.openai.OpenAiChatModel;
import org.springframework.ai.openai.OpenAiChatOptions;
import org.springframework.ai.openai.api.OpenAiApi;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.retry.support.RetryTemplate;

import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.function.Function;
import java.util.stream.Collectors;

/**
 * Spring AI 多 provider 配置。
 * 这里手动创建多个 ChatClient，避免单一 provider 自动配置限制。
 */
@Configuration
@EnableConfigurationProperties(LlmProperties.class)
public class LlmSpringAiConfig {

    @Bean(destroyMethod = "shutdown")
    public ExecutorService llmExecutorService() {
        return Executors.newVirtualThreadPerTaskExecutor();
    }

    @Bean("openaiChatClient")
    public ChatClient openaiChatClient(LlmProperties properties) {
        LlmProperties.ProviderProperties provider = properties.requiredProvider("openai");

        OpenAiApi openAiApi = OpenAiApi.builder()
                .apiKey(provider.apiKey())
                .baseUrl(provider.baseUrl())
                .completionsPath(provider.completionsPath())
                .build();

        OpenAiChatOptions options = OpenAiChatOptions.builder()
                .model(provider.model())
                .temperature(provider.temperatureOrDefault())
                .maxTokens(provider.maxTokensOrDefault())
                .build();

        OpenAiChatModel model = OpenAiChatModel.builder()
                .openAiApi(openAiApi)
                .defaultOptions(options)
                .build();

        return ChatClient.builder(model).build();
    }

    @Bean("deepseekChatClient")
    public ChatClient deepseekChatClient(LlmProperties properties) {
        LlmProperties.ProviderProperties provider = properties.requiredProvider("deepseek");

        OpenAiApi deepseekApi = OpenAiApi.builder()
                .apiKey(provider.apiKey())
                .baseUrl(provider.baseUrl())
                .completionsPath(provider.completionsPath())
                .build();

        OpenAiChatOptions options = OpenAiChatOptions.builder()
                .model(provider.model())
                .temperature(provider.temperatureOrDefault())
                .maxTokens(provider.maxTokensOrDefault())
                .build();

        OpenAiChatModel model = OpenAiChatModel.builder()
                .openAiApi(deepseekApi)
                .defaultOptions(options)
                .build();

        return ChatClient.builder(model).build();
    }

    @Bean("anthropicChatClient")
    public ChatClient anthropicChatClient(LlmProperties properties) {
        LlmProperties.ProviderProperties provider = properties.requiredProvider("anthropic");

        AnthropicApi anthropicApi = AnthropicApi.builder()
                .apiKey(provider.apiKey())
                .baseUrl(provider.baseUrl())
                .completionsPath(provider.completionsPath())
                .anthropicVersion(provider.anthropicVersion())
                .build();

        AnthropicChatOptions options = AnthropicChatOptions.builder()
                .model(provider.model())
                .temperature(provider.temperatureOrDefault())
                .maxTokens(provider.maxTokensOrDefault())
                .build();

        AnthropicChatModel model = new AnthropicChatModel(
                anthropicApi,
                options,
                ToolCallingManager.builder().build(),
                new RetryTemplate(),
                ObservationRegistry.create()
        );

        return ChatClient.builder(model).build();
    }

    @Bean
    public LlmProviderClient openaiProviderClient(
            LlmProperties properties,
            ExecutorService llmExecutorService,
            ChatClient openaiChatClient
    ) {
        LlmProperties.ProviderProperties provider = properties.requiredProvider("openai");

        return new SpringAiProviderClient(
                "openai",
                LlmProvider.OPENAI,
                provider.model(),
                openaiChatClient,
                Duration.ofSeconds(provider.requestTimeoutSecondsOrDefault()),
                provider.maxRetriesOrDefault(),
                llmExecutorService
        );
    }

    @Bean
    public LlmProviderClient deepseekProviderClient(
            LlmProperties properties,
            ExecutorService llmExecutorService,
            ChatClient deepseekChatClient
    ) {
        LlmProperties.ProviderProperties provider = properties.requiredProvider("deepseek");

        return new SpringAiProviderClient(
                "deepseek",
                LlmProvider.DEEPSEEK,
                provider.model(),
                deepseekChatClient,
                Duration.ofSeconds(provider.requestTimeoutSecondsOrDefault()),
                provider.maxRetriesOrDefault(),
                llmExecutorService
        );
    }

    @Bean
    public LlmProviderClient anthropicProviderClient(
            LlmProperties properties,
            ExecutorService llmExecutorService,
            ChatClient anthropicChatClient
    ) {
        LlmProperties.ProviderProperties provider = properties.requiredProvider("anthropic");

        return new SpringAiProviderClient(
                "anthropic",
                LlmProvider.ANTHROPIC,
                provider.model(),
                anthropicChatClient,
                Duration.ofSeconds(provider.requestTimeoutSecondsOrDefault()),
                provider.maxRetriesOrDefault(),
                llmExecutorService
        );
    }

    @Bean
    public ProviderFallbackRouter providerFallbackRouter(
            List<LlmProviderClient> clients,
            LlmProperties properties
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
                        throw new IllegalStateException("No LlmProviderClient found: " + providerName);
                    }

                    return client;
                })
                .toList();

        return new ProviderFallbackRouter(orderedClients);
    }
}
```
