# 调用 OpenAI-compatible API

用 Spring 官方的 `WebClient` 处理 HTTP 调用。

流式调用的核心变化是：

1. 请求体 stream = true
2. 响应类型从普通 JSON 变成 text/event-stream
3. 每个 SSE 事件里解析 `choices[].delta.content`
4. 遇到 `[DONE]` 表示流结束

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

关键区别是：

1. 非流式：
   ```java
   stream = false
   bodyToMono(OpenAiChatResponse.class)
   choices[].message.content
   ```
2. 流式：
   ```java
   stream = true
   bodyToFlux(ServerSentEvent<String>)
   choices[].delta.content
   data: [DONE] 表示结束
   ```

注意：流式响应里不能再按 choices[].message.content 取值。每个 chunk 只是一小段增量内容，应该取：

```java
choices[0].delta.content
```

```java
package com.example.demo;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerSentEvent;
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
     * 适用于 OpenAI 风格的流式响应体 DTO。
     *
     * 流式响应不是一次性返回完整 message，
     * 而是每个 SSE 事件返回一小段 delta。
     */
    @JsonIgnoreProperties(ignoreUnknown = true)
    public record OpenAiChatStreamResponse(
            List<Choice> choices // 候选增量列表
    ) {
        /**
         * 获取当前 chunk 的增量文本。
         * 没有文本时返回空字符串，避免调用方空指针。
         */
        public String deltaText() {
            if (choices == null || choices.isEmpty()) {
                return "";
            }

            Delta delta = choices.getFirst().delta();

            if (delta == null || delta.content() == null) {
                return "";
            }

            return delta.content();
        }

        /**
         * 单个候选增量。
         */
        @JsonIgnoreProperties(ignoreUnknown = true)
        public record Choice(
                Delta delta, // 当前增量内容
                @JsonProperty("finish_reason") String finishReason // 结束原因，未结束时通常为 null
        ) {
        }

        /**
         * 模型返回的增量内容。
         *
         * 第一个 chunk 可能只有 role，没有 content。
         * 后续 chunk 才会逐步返回 content。
         */
        @JsonIgnoreProperties(ignoreUnknown = true)
        public record Delta(
                String role, // role 通常是 assistant，且一般只在第一个 chunk 出现
                String content // 当前增量文本
        ) {
        }
    }

    // WebClient 构建器，用于创建 HTTP 客户端。
    private final WebClient.Builder webClientBuilder;

    // Jackson JSON 解析器，用于解析每个 SSE data 里的 JSON 字符串。
    private final ObjectMapper objectMapper;

    public DemoConsole(
            WebClient.Builder webClientBuilder,
            ObjectMapper objectMapper
    ) {
        this.webClientBuilder = webClientBuilder;
        this.objectMapper = objectMapper;
    }

    /**
     * 入口
     */
    @Override
    public void run(String... args) {
        String API_KEY = "换成你自己的KEY";

        // 要发给大模型的消息。
        List<LlmMessage> messages = List.of(
                LlmMessage.system("你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。"),
                LlmMessage.user("用一句话解释什么是 RAG。")
        );

        WebClient webClient = webClientBuilder
                // 以 DeepSeek 为例。
                .baseUrl("https://api.deepseek.com")
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + API_KEY)
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();

        // 构造 OpenAI-compatible 流式请求体。
        OpenAiChatRequest request = new OpenAiChatRequest(
                "deepseek-v4-pro", // 模型
                messages, // 对话列表
                0.2, // temperature
                1000, // max_tokens
                true // 启用流式输出
        );

        // 发送请求并按 SSE 事件逐个读取。
        webClient.post()
                .uri("/chat/completions")
                .accept(MediaType.TEXT_EVENT_STREAM)
                .bodyValue(request)
                .retrieve()
                .bodyToFlux(new ParameterizedTypeReference<ServerSentEvent<String>>() {})
                .timeout(Duration.ofSeconds(60))
                .doOnNext(event -> {
                    String data = event.data();

                    if (data == null || data.isBlank()) {
                        return;
                    }

                    // OpenAI-compatible 流式响应通常用 [DONE] 表示结束。
                    if ("[DONE]".equals(data)) {
                        return;
                    }

                    try {
                        OpenAiChatStreamResponse chunk = objectMapper.readValue(
                                data,
                                OpenAiChatStreamResponse.class
                        );

                        String text = chunk.deltaText();

                        if (!text.isEmpty()) {
                            // print 不换行，模拟 token-by-token 输出效果。
                            System.out.print(text);
                        }
                    } catch (Exception e) {
                        throw new RuntimeException("解析流式响应失败，data = " + data, e);
                    }
                })
                .blockLast();

        // 流式输出结束后补一个换行。
        System.out.println();
    }
}
```
