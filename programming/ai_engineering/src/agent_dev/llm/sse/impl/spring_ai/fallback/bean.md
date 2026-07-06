# 创建 Bean

```java id="ofy3y4"
package com.example.llm.config;

import com.example.llm.dto.LlmProvider;
import com.example.llm.provider.LlmStreamProviderClient;
import com.example.llm.provider.SpringAiStreamProviderClient;
import com.example.llm.router.StreamProviderFallbackRouter;
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

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

/**
 * 手动创建 Spring AI ChatModel / ChatClient / ProviderClient / Router。
 */
@Configuration
@EnableConfigurationProperties(LlmProperties.class)
public class SpringAiStreamProviderConfig {

    @Bean
    public LlmStreamProviderClient openAiSpringAiStreamProviderClient(
            LlmProperties properties
    ) {
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

        ChatClient chatClient = ChatClient.builder(model).build();

        return new SpringAiStreamProviderClient(
                "openai",
                LlmProvider.OPENAI,
                provider.model(),
                chatClient,
                provider.streamIdleTimeoutSecondsOrDefault(),
                provider.maxRetriesOrDefault()
        );
    }

    @Bean
    public LlmStreamProviderClient deepSeekSpringAiStreamProviderClient(
            LlmProperties properties
    ) {
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

        ChatClient chatClient = ChatClient.builder(model).build();

        return new SpringAiStreamProviderClient(
                "deepseek",
                LlmProvider.DEEPSEEK,
                provider.model(),
                chatClient,
                provider.streamIdleTimeoutSecondsOrDefault(),
                provider.maxRetriesOrDefault()
        );
    }

    @Bean
    public LlmStreamProviderClient anthropicSpringAiStreamProviderClient(
            LlmProperties properties
    ) {
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

        ChatClient chatClient = ChatClient.builder(model).build();

        return new SpringAiStreamProviderClient(
                "anthropic",
                LlmProvider.ANTHROPIC,
                provider.model(),
                chatClient,
                provider.streamIdleTimeoutSecondsOrDefault(),
                provider.maxRetriesOrDefault()
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
