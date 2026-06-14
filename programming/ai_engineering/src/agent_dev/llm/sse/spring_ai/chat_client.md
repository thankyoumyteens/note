# 创建多个 ChatClient

多 provider 的关键是：不要只注入一个默认 `ChatClient.Builder` 就完事。你要显式创建三个 `ChatClient`。

```java
package com.example.ai.config;

import io.micrometer.observation.ObservationRegistry;
import org.springframework.ai.anthropic.AnthropicChatModel;
import org.springframework.ai.anthropic.AnthropicChatOptions;
import org.springframework.ai.anthropic.api.AnthropicApi;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.model.tool.ToolCallingManager;
import org.springframework.ai.openai.OpenAiChatModel;
import org.springframework.ai.openai.OpenAiChatOptions;
import org.springframework.ai.openai.api.OpenAiApi;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.retry.support.RetryTemplate;

/**
 * 手动创建多个 ChatClient。
 * 不依赖 Spring AI starter 自动配置。
 */
@Configuration
public class MultiProviderChatClientConfig {

    @Bean
    @Primary
    public ChatClient deepSeekChatClient(AiProviderProperties properties) {
        var provider = properties.getRequiredProvider("deepseek");

        // 连接层配置：API Key、base-url、Chat Completions 路径。
        OpenAiApi deepseekApi = OpenAiApi.builder()
                .apiKey(provider.apiKey())
                .baseUrl(provider.baseUrl())
                .completionsPath(provider.completionsPath())
                .build();

        // 模型参数配置：模型名、温度、最大输出 token。
        OpenAiChatOptions options = OpenAiChatOptions.builder()
                .model(provider.model())
                .temperature(provider.temperature())
                .maxTokens(provider.maxTokens())
                .build();

        // DeepSeek 走 OpenAI-compatible 协议，所以使用 OpenAiChatModel。
        OpenAiChatModel model = OpenAiChatModel.builder()
                .openAiApi(deepseekApi)
                .defaultOptions(options)
                .build();

        return ChatClient.builder(model)
                .defaultSystem("你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。")
                .build();
    }

    @Bean
    public ChatClient openAiChatClient(AiProviderProperties properties) {
        var provider = properties.getRequiredProvider("openai");

        // OpenAI 官方连接配置。
        OpenAiApi openAiApi = OpenAiApi.builder()
                .apiKey(provider.apiKey())
                .baseUrl(provider.baseUrl())
                .completionsPath(provider.completionsPath())
                .build();

        // OpenAI 模型参数配置。
        OpenAiChatOptions options = OpenAiChatOptions.builder()
                .model(provider.model())
                .temperature(provider.temperature())
                .maxTokens(provider.maxTokens())
                .build();

        OpenAiChatModel model = OpenAiChatModel.builder()
                .openAiApi(openAiApi)
                .defaultOptions(options)
                .build();

        return ChatClient.builder(model)
                .defaultSystem("你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。")
                .build();
    }

    @Bean
    public ChatClient claudeChatClient(AiProviderProperties properties) {
        var provider = properties.getRequiredProvider("claude");

        // 连接层配置：API Key、base-url、接口路径、Anthropic API 版本。
        AnthropicApi anthropicApi = AnthropicApi.builder()
                .apiKey(provider.apiKey())
                .baseUrl(provider.baseUrl())
                .completionsPath(provider.completionsPath())
                .anthropicVersion(provider.version())
                .build();

        // 模型参数配置：模型名、温度、最大输出 token。
        AnthropicChatOptions options = AnthropicChatOptions.builder()
                .model(provider.model())
                .temperature(provider.temperature())
                .maxTokens(provider.maxTokens())
                .build();

        // ToolCallingManager 负责 Spring AI 的工具调用管理。
        ToolCallingManager toolCallingManager = ToolCallingManager.builder().build();

        // RetryTemplate 负责请求失败后的重试逻辑；这里先用默认配置。
        RetryTemplate retryTemplate = new RetryTemplate();

        // ObservationRegistry 负责 Micrometer 观测能力；这里先创建默认 registry。
        ObservationRegistry observationRegistry = ObservationRegistry.create();

        AnthropicChatModel model = new AnthropicChatModel(
                anthropicApi,
                options,
                toolCallingManager,
                retryTemplate,
                observationRegistry
        );

        return ChatClient.builder(model)
                .defaultSystem("你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。")
                .build();
    }
}
```
