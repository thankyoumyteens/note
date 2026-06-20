# 调用 OpenAI Responses API

Responses API 使用 `POST /v1/responses` 创建模型响应；`input` 可以直接传字符串，等价于 user 文本输入；`instructions` 用于放入 system/developer 类指令；`max_output_tokens` 用于限制模型最多生成的 token 数。

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
     * Responses API 请求体。
     * input 可以直接传字符串，表示一次用户输入。
     */
    @JsonInclude(JsonInclude.Include.NON_NULL)
    public record OpenAiResponsesRequest(
            String model, // 要调用的模型名称
            String instructions, // system / developer 类指令
            String input, // 用户输入
            Double temperature, // 控制模型输出随机性的参数
            @JsonProperty("max_output_tokens") Integer maxOutputTokens, // 限制模型最多生成多少 token
            Boolean stream // 是否启用流式输出
    ) {
    }

    /**
     * Responses API 响应体。
     * 普通文本输出通常在 output[].content[] 中，type 为 output_text。
     */
    public record OpenAiResponsesResponse(
            String id, // response id
            String model, // 实际使用的模型
            List<OutputItem> output // 输出列表
    ) {

        /**
         * 获取第一个 output_text 文本。
         * 如果响应为空或没有文本，则返回空字符串，避免空指针异常。
         */
        public String firstText() {
            if (output == null || output.isEmpty()) {
                return "";
            }

            StringBuilder builder = new StringBuilder();

            for (OutputItem outputItem : output) {
                if (outputItem.content() == null || outputItem.content().isEmpty()) {
                    continue;
                }

                for (ContentItem contentItem : outputItem.content()) {
                    if ("output_text".equals(contentItem.type()) && contentItem.text() != null) {
                        builder.append(contentItem.text());
                    }
                }
            }

            return builder.toString();
        }

        /**
         * 单个输出项。
         * 普通文本回答一般是 type = message。
         */
        public record OutputItem(
                String type, // 输出项类型
                List<ContentItem> content // 输出内容块
        ) {
        }

        /**
         * 输出内容块。
         * 文本结果通常是 type = output_text。
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
                .baseUrl("https://api.openai.com/v1")
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + API_KEY)
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();

        // 构造 Responses API 请求体。
        OpenAiResponsesRequest request = new OpenAiResponsesRequest(
                "gpt-4o-mini", // 模型。如果你的账号不可用，换成你账号有权限的模型。
                "你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。", // instructions
                "用一句话解释什么是 RAG。", // input
                0.2, // temperature
                1000, // max_output_tokens
                false // 不使用流式输出
        );

        // 发送请求并把响应反序列化为 OpenAiResponsesResponse。
        OpenAiResponsesResponse response = webClient.post()
                .uri("/responses")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(OpenAiResponsesResponse.class)
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
