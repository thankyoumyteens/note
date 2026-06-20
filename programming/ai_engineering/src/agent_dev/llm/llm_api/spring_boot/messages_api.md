# 调用 Anthropic Messages API

Anthropic Messages API 使用 `POST /v1/messages` 创建模型响应；`messages` 用于放入 user / assistant 对话历史；`system` 是顶层字段，用于放入 system 指令；`max_tokens` 是必填字段，用于限制模型最多生成的 token 数。调用 Anthropic 官方 API 时，需要使用 `x-api-key` 请求头，并且需要传 `anthropic-version`，常用版本是 `2023-06-01`。

## maven 依赖

```xml
<dependencies>
    <!-- Spring Boot Web API -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <!-- WebClient -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-webflux</artifactId>
    </dependency>

    <!--
        配置属性绑定
        在编译时扫描 @ConfigurationProperties 配置类，生成配置元数据，
        让 IDEA / VS Code 等 IDE 在 application.yml 或 application.properties 里提供自动补全、跳转、类型提示和说明。
        它主要服务于开发体验，不是业务运行逻辑。
     -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-configuration-processor</artifactId>
        <optional>true</optional>
    </dependency>
</dependencies>
```

## 代码

```java
package com.example.demo;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import org.springframework.boot.CommandLineRunner;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.util.List;

@Component
public class DemoConsole implements CommandLineRunner {

    /**
     * Anthropic Messages API 请求体。
     * system 是顶层字段，不放在 messages 数组里。
     */
    @JsonInclude(JsonInclude.Include.NON_NULL)
    public record AnthropicMessagesRequest(
            String model, // 要调用的 Claude 模型名称
            String system, // system 指令
            List<Message> messages, // 对话消息列表
            @JsonProperty("max_tokens") Integer maxTokens, // 限制模型最多生成多少 token
            Boolean stream // 是否启用流式输出
    ) {
    }

    /**
     * 单条对话消息。
     * role 通常是 user 或 assistant。
     */
    public record Message(
            String role, // 消息角色：user / assistant
            String content // 消息文本内容
    ) {
    }

    /**
     * Anthropic Messages API 响应体。
     * 普通文本输出通常在 content[] 中，type 为 text。
     */
    public record AnthropicMessagesResponse(
            String id, // message id
            String type, // 响应类型，通常是 message
            String role, // 返回角色，通常是 assistant
            String model, // 实际使用的模型
            List<ContentItem> content, // 输出内容块
            @JsonProperty("stop_reason") String stopReason // 停止原因，例如 end_turn
    ) {

        /**
         * 获取所有 text 内容。
         * 如果响应为空或没有文本，则返回空字符串，避免空指针异常。
         */
        public String firstText() {
            if (content == null || content.isEmpty()) {
                return "";
            }

            StringBuilder builder = new StringBuilder();

            for (ContentItem contentItem : content) {
                if ("text".equals(contentItem.type()) && contentItem.text() != null) {
                    builder.append(contentItem.text());
                }
            }

            return builder.toString();
        }

        /**
         * 输出内容块。
         * 普通文本回答一般是 type = text。
         */
        public record ContentItem(
                String type, // 内容类型
                String text // 文本内容
        ) {
        }
    }

    // WebClient 构建器，用于创建 HTTP 客户端。
    private final WebClient.Builder webClientBuilder;

    public DemoConsole(WebClient.Builder webClientBuilder) {
        this.webClientBuilder = webClientBuilder;
    }

    /**
     * 入口
     */
    @Override
    public void run(String... args) {
        String API_KEY = "换成你自己的KEY";

        WebClient webClient = webClientBuilder
                .baseUrl("https://api.anthropic.com/v1")
                .defaultHeader("x-api-key", API_KEY)
                .defaultHeader("anthropic-version", "2023-06-01")
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();

        // 构造 Messages API 请求体。
        AnthropicMessagesRequest request = new AnthropicMessagesRequest(
                "claude-sonnet-4-5", // 模型。如果你的账号不可用，换成你账号有权限的模型。
                "你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。", // system
                List.of(
                        new Message(
                                "user",
                                "用一句话解释什么是 RAG。"
                        )
                ),
                1000, // max_tokens
                false // 不使用流式输出
        );

        // 发送请求并把响应反序列化为 AnthropicMessagesResponse。
        AnthropicMessagesResponse response = webClient.post()
                .uri("/messages")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(AnthropicMessagesResponse.class)
                .timeout(Duration.ofSeconds(60))
                .block();

        if (response == null) {
            throw new RuntimeException("大模型没有返回");
        }

        // 提取模型最终文本。
        System.out.println(response.firstText());
    }
}
```
