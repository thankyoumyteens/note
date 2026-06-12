# 统一 LLM Client

## 接口

```java
package com.example.llm;

/**
 * 统一的 LLM 客户端接口。
 * 用于屏蔽 OpenAI、Claude、Qwen、DeepSeek 等不同模型 API 的调用差异。
 */
public interface LlmClient {

    /**
     * 调用指定 provider 的模型进行普通聊天。
     *
     * @param provider    模型服务商标识，例如 openai、claude、qwen、deepseek
     * @param userMessage 用户输入内容
     * @return 模型返回的文本回答
     */
    String chat(String provider, String userMessage);
}
```

## 实现

```java
package com.example.llm;

import com.example.llm.config.LlmProperties;
import com.example.llm.dto.LlmMessage;
import com.example.llm.dto.claude.ClaudeMessageRequest;
import com.example.llm.dto.claude.ClaudeMessageResponse;
import com.example.llm.dto.openai.OpenAiChatRequest;
import com.example.llm.dto.openai.OpenAiChatResponse;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.util.List;
import java.util.Objects;

/**
 * 默认的 LLM 客户端实现。
 * 根据 provider 配置路由到 OpenAI-compatible 或 Claude API。
 */
@Service
public class DefaultLlmClient implements LlmClient {

    /**
     * WebClient 构建器，用于创建不同 provider 的 HTTP 客户端。
     */
    private final WebClient.Builder webClientBuilder;

    /**
     * LLM 配置，包含默认 provider、baseUrl、apiKey、model 等信息。
     */
    private final LlmProperties llmProperties;

    public DefaultLlmClient(WebClient.Builder webClientBuilder,
                            LlmProperties llmProperties) {
        this.webClientBuilder = webClientBuilder;
        this.llmProperties = llmProperties;
    }

    /**
     * 对外统一的聊天入口。
     * 如果 provider 为空，则使用配置中的默认 provider。
     */
    @Override
    public String chat(String provider, String userMessage) {
        String providerName = provider == null || provider.isBlank()
                ? llmProperties.defaultProvider()
                : provider;

        // 根据 provider 名称读取对应模型配置。
        LlmProperties.ProviderConfig config = llmProperties.providers().get(providerName);

        if (config == null) {
            throw new IllegalArgumentException("Unknown LLM provider: " + providerName);
        }

        // 构造统一消息列表，后续不同 provider 会按各自格式转换。
        List<LlmMessage> messages = List.of(
                LlmMessage.system("你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。"),
                LlmMessage.user(userMessage)
        );

        // 根据 provider 类型选择不同 API 调用方式。
        return switch (config.type()) {
            case "openai-compatible" -> callOpenAiCompatible(config, messages);
            case "anthropic" -> callClaude(config, messages);
            default -> throw new IllegalArgumentException("Unsupported LLM provider type: " + config.type());
        };
    }
}
```

### callOpenAiCompatible

```java
/**
 * 调用 OpenAI-compatible Chat Completions API。
 * 适用于 OpenAI、Qwen、DeepSeek 等兼容 /chat/completions 的服务。
 */
private String callOpenAiCompatible(LlmProperties.ProviderConfig config,
                                    List<LlmMessage> messages) {
    WebClient webClient = webClientBuilder
            .baseUrl(config.baseUrl())
            .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + config.apiKey())
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .build();

    // 构造 OpenAI-compatible 请求体。
    OpenAiChatRequest request = new OpenAiChatRequest(
            config.model(),
            messages,
            0.2,
            1000,
            false
    );

    // 发送请求并把响应反序列化为 OpenAiChatResponse。
    OpenAiChatResponse response = webClient.post()
            .uri("/chat/completions")
            .bodyValue(request)
            .retrieve()
            .bodyToMono(OpenAiChatResponse.class)
            .timeout(Duration.ofSeconds(60))
            .block();

    if (response == null) {
        return "";
    }

    // 提取第一个候选回答的文本内容。
    return response.firstText();
}
```

### callClaude

```java
/**
 * 调用 Claude Messages API。
 * Claude 原生 API 的 system 字段需要从 messages 中单独拆出来。
 */
private String callClaude(LlmProperties.ProviderConfig config,
                            List<LlmMessage> messages) {
    WebClient webClient = webClientBuilder
            .baseUrl(config.baseUrl())
            .defaultHeader("x-api-key", config.apiKey())
            .defaultHeader("anthropic-version", "2023-06-01")
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .build();

    // Claude 的 system 是独立字段，不放在 messages 数组里。
    String system = messages.stream()
            .filter(message -> Objects.equals(message.role(), "system"))
            .map(LlmMessage::content)
            .findFirst()
            .orElse(null);

    // Claude messages 只保留 user / assistant 消息。
    List<LlmMessage> claudeMessages = messages.stream()
            .filter(message -> !Objects.equals(message.role(), "system"))
            .toList();

    // 构造 Claude Messages API 请求体。
    ClaudeMessageRequest request = new ClaudeMessageRequest(
            config.model(),
            1000,
            system,
            claudeMessages
    );

    // 发送请求并把响应反序列化为 ClaudeMessageResponse。
    ClaudeMessageResponse response = webClient.post()
            .uri("/messages")
            .bodyValue(request)
            .retrieve()
            .bodyToMono(ClaudeMessageResponse.class)
            .timeout(Duration.ofSeconds(60))
            .block();

    if (response == null) {
        return "";
    }

    // 提取 Claude 返回的文本内容。
    return response.text();
}
```
