# 调用 OpenAI-compatible API

用 Spring 官方的 `WebClient` 处理 HTTP 调用。

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
     * 统一的 LLM 消息对象，用于表示一条对话消息。
     */
    public record LlmMessage(
            String role, // 消息角色
            String content // 消息内容
    ) {
        // 创建 system 消息，用于设置模型行为和回答规则。
        public static LlmMessage system(String content) {
            return new LlmMessage("system", content);
        }

        // 创建 user 消息，用于表示用户输入。
        public static LlmMessage user(String content) {
            return new LlmMessage("user", content);
        }

        // 创建 assistant 消息，用于表示模型历史回复。
        public static LlmMessage assistant(String content) {
            return new LlmMessage("assistant", content);
        }
    }

    /**
     * 适用于 OpenAI 风格的请求体 DTO。
     */
    @JsonInclude(JsonInclude.Include.NON_NULL)
    public record OpenAiChatRequest(
            String model, // 要调用的模型名称
            List<LlmMessage> messages, // 对话消息列表
            Double temperature, // 控制模型输出随机性的参数
            @JsonProperty("max_tokens") Integer maxTokens, // 限制模型最多生成多少 token
            Boolean stream // 是否启用流式输出
    ) {
    }

    /**
     * 适用于 OpenAI 风格的响应体 DTO。
     */
    public record OpenAiChatResponse(
            List<Choice> choices
    ) {
        // 获取第一个候选回答的文本内容
        public String firstText() {
            if (choices == null || choices.isEmpty()) return "";
            // 普通聊天场景通常只取第一个候选结果。
            Message message = choices.getFirst().message();
            // message 或 content 为空时返回空字符串，保证调用方拿到稳定的 String。
            return message == null || message.content() == null ? "" : message.content();
        }

        /**
         * 单个候选结果。
         */
        public record Choice(
                Message message // 当前只关心其中的 message 字段
        ) {
        }

        /**
         * 模型返回的消息内容。
         */
        public record Message(
                String role, // role 通常是 assistant
                String content // content 是模型最终的回答
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
        // 要发给大模型的消息
        List<LlmMessage> messages = List.of(
                LlmMessage.system("你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。"),
                LlmMessage.user("用一句话解释什么是 RAG。")
        );
        WebClient webClient = webClientBuilder
                // 以 DeepSeek 为例
                .baseUrl("https://api.deepseek.com")
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + API_KEY)
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();
        // 构造 OpenAI-compatible 请求体。
        OpenAiChatRequest request = new OpenAiChatRequest(
                "deepseek-v4-pro", // 模型
                messages, // 对话列表
                0.2, // temperature
                1000, // max_tokens
                false // 不使用流式输出
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
            throw new RuntimeException("大模型没有返回");
        }
        // 提取第一个候选回答的文本内容。
        System.out.println(response.firstText());
    }
}
```
