# 调用 OpenAI Responses API

Responses API 的流式输出不是一次性返回完整 `output[].content[].text`，而是返回一组 SSE 事件。最常用的是：

- response.created
- response.output_text.delta
- response.completed
- error

其中，真正的增量文本在 `response.output_text.delta` 事件的 delta 字段里。

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
   bodyToMono(OpenAiResponsesResponse.class)
   output[].content[].text
   ```
2. 流式：
   ```java
   stream = true
   bodyToFlux(ServerSentEvent<String>)
   只处理 response.output_text.delta
   读取 delta 字段
   ```

也就是流式版本不要再找：

```java
output[].content[].text
```

而是读取每个事件中的：

```java
type = response.output_text.delta
delta = 当前增量文本
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
     * Responses API 流式事件。
     *
     * Responses API 流式返回的是一系列事件，
     * 常见事件类型包括：
     * response.created
     * response.output_text.delta
     * response.completed
     * error
     */
    @JsonIgnoreProperties(ignoreUnknown = true)
    public record OpenAiResponsesStreamEvent(
            String type, // 事件类型，例如 response.output_text.delta
            String delta, // 增量文本，只在 response.output_text.delta 中重点使用
            ErrorInfo error // 错误信息，只在 error 事件中重点使用
    ) {
        /**
         * 判断当前事件是否是文本增量事件。
         * 有些 SSE 客户端会把事件名放在 event 字段里，
         * 有些场景只需要读取 data JSON 里的 type 字段。
         */
        public boolean isTextDelta(String sseEventName) {
            String eventType = type != null ? type : sseEventName;
            return "response.output_text.delta".equals(eventType);
        }

        /**
         * 判断当前事件是否是错误事件。
         */
        public boolean isError(String sseEventName) {
            String eventType = type != null ? type : sseEventName;
            return "error".equals(eventType);
        }

        /**
         * 错误信息。
         */
        @JsonIgnoreProperties(ignoreUnknown = true)
        public record ErrorInfo(
                String type, // 错误类型
                String code, // 错误码
                String message // 错误消息
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

        WebClient webClient = webClientBuilder
                .baseUrl("https://api.openai.com/v1")
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + API_KEY)
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();

        // 构造 Responses API 流式请求体。
        OpenAiResponsesRequest request = new OpenAiResponsesRequest(
                "gpt-4o-mini", // 模型。如果你的账号不可用，换成你账号有权限的模型。
                "你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。", // instructions
                "用一句话解释什么是 RAG。", // input
                0.2, // temperature
                1000, // max_output_tokens
                true // 启用流式输出
        );

        // 发送请求并按 SSE 事件逐个读取。
        webClient.post()
                .uri("/responses")
                .accept(MediaType.TEXT_EVENT_STREAM)
                .bodyValue(request)
                .retrieve()
                .bodyToFlux(new ParameterizedTypeReference<ServerSentEvent<String>>() {})
                .timeout(Duration.ofSeconds(60))
                .doOnNext(event -> {
                    String sseEventName = event.event();
                    String data = event.data();

                    if (data == null || data.isBlank()) {
                        return;
                    }

                    // 兼容部分 SSE 实现可能返回的结束标记。
                    if ("[DONE]".equals(data)) {
                        return;
                    }

                    try {
                        OpenAiResponsesStreamEvent streamEvent = objectMapper.readValue(
                                data,
                                OpenAiResponsesStreamEvent.class
                        );

                        if (streamEvent.isTextDelta(sseEventName)) {
                            String text = streamEvent.delta();

                            if (text != null && !text.isEmpty()) {
                                // print 不换行，模拟 token-by-token 输出效果。
                                System.out.print(text);
                            }

                            return;
                        }

                        if (streamEvent.isError(sseEventName)) {
                            OpenAiResponsesStreamEvent.ErrorInfo error = streamEvent.error();

                            if (error == null) {
                                throw new RuntimeException("Responses API 流式调用返回 error 事件");
                            }

                            throw new RuntimeException(
                                    "Responses API 流式调用失败：" + error.message()
                            );
                        }

                        // 其它事件，例如 response.created / response.completed，
                        // 当前示例不处理，只忽略。
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
