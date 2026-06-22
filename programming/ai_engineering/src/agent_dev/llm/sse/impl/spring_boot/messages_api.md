# 调用 Anthropic Messages API

Anthropic Messages API 开启流式输出时，需要在请求体中设置 stream: true，服务端会通过 SSE 返回一系列命名事件。常见事件包括

- message_start
- content_block_start
- content_block_delta
- content_block_stop
- message_delta
- message_stop
- ping
- error

真正的文本增量通常在 content_block_delta 事件的 delta.text 字段里。

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
   bodyToMono(AnthropicMessagesResponse.class)
   content[].text
   ```
2. 流式：
   ```java
   stream = true
   bodyToFlux(ServerSentEvent<String>)
   只处理 content_block_delta
   读取 delta.text
   message_stop 表示消息结束
   ```

也就是流式版本不要再找：

```java
content[].text
```

而是读取每个事件中的：

```java
type = content_block_delta
delta.type = text_delta
delta.text = 当前增量文本
```

另外，Anthropic 的流式响应不应该按 OpenAI-compatible 的 `[DONE]` 来判断结束；在 2023-06-01 版本中，结束事件是命名 SSE 事件 message_stop。

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
     * Anthropic Messages API 流式事件。
     */
    @JsonIgnoreProperties(ignoreUnknown = true)
    public record AnthropicStreamEvent(
            String type, // 事件类型，例如 content_block_delta
            Integer index, // content block 的索引
            Delta delta, // 增量内容，文本增量在 delta.text
            ErrorInfo error // 错误信息，只在 error 事件中重点使用
    ) {
        /**
         * 判断当前事件是否是文本增量事件。
         * SSE event 名和 data.type 通常一致，这里两者都兼容。
         */
        public boolean isTextDelta(String sseEventName) {
            String eventType = type != null ? type : sseEventName;

            return "content_block_delta".equals(eventType)
                    && delta != null
                    && "text_delta".equals(delta.type())
                    && delta.text() != null;
        }

        /**
         * 判断当前事件是否是错误事件。
         */
        public boolean isError(String sseEventName) {
            String eventType = type != null ? type : sseEventName;
            return "error".equals(eventType);
        }

        /**
         * 判断当前事件是否是消息结束事件。
         */
        public boolean isMessageStop(String sseEventName) {
            String eventType = type != null ? type : sseEventName;
            return "message_stop".equals(eventType);
        }

        /**
         * 增量内容。
         *
         * 普通文本输出：
         * delta.type = text_delta
         * delta.text = 当前增量文本
         *
         * 如果开启 extended thinking，可能还会出现 thinking_delta。
         * 如果使用 tool use，可能还会出现 input_json_delta。
         */
        @JsonIgnoreProperties(ignoreUnknown = true)
        public record Delta(
                String type, // text_delta / thinking_delta / input_json_delta 等
                String text, // text_delta 对应的增量文本
                @JsonProperty("partial_json") String partialJson // tool use 场景的增量 JSON
        ) {
        }

        /**
         * 错误信息。
         */
        @JsonIgnoreProperties(ignoreUnknown = true)
        public record ErrorInfo(
                String type, // 错误类型
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
                .baseUrl("https://api.anthropic.com/v1")
                .defaultHeader("x-api-key", API_KEY)
                .defaultHeader("anthropic-version", "2023-06-01")
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();

        // 构造 Messages API 流式请求体。
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
                true // 启用流式输出
        );

        // 发送请求并按 SSE 事件逐个读取。
        webClient.post()
                .uri("/messages")
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

                    AnthropicStreamEvent streamEvent;

                    try {
                        streamEvent = objectMapper.readValue(
                                data,
                                AnthropicStreamEvent.class
                        );
                    } catch (Exception e) {
                        throw new RuntimeException("解析流式响应失败，data = " + data, e);
                    }

                    if (streamEvent.isTextDelta(sseEventName)) {
                        String text = streamEvent.delta().text();

                        if (!text.isEmpty()) {
                            // print 不换行，模拟 token-by-token 输出效果。
                            System.out.print(text);
                        }

                        return;
                    }

                    if (streamEvent.isError(sseEventName)) {
                        AnthropicStreamEvent.ErrorInfo error = streamEvent.error();

                        if (error == null) {
                            throw new RuntimeException("Anthropic Messages API 流式调用返回 error 事件");
                        }

                        throw new RuntimeException(
                                "Anthropic Messages API 流式调用失败：" + error.message()
                        );
                    }

                    if (streamEvent.isMessageStop(sseEventName)) {
                        // message_stop 表示模型消息已经结束。
                        // 这里不用手动关闭流，WebClient 会在 HTTP 流结束后自然完成。
                        return;
                    }

                    // 其它事件，例如 message_start / content_block_start / content_block_stop /
                    // message_delta / ping，当前示例不处理，只忽略。
                })
                .blockLast();

        // 流式输出结束后补一个换行。
        System.out.println();
    }
}
```
