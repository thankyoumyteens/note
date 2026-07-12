# 调用 Anthropic Messages API

Anthropic Messages API 使用 `POST /v1/messages` 创建模型响应；`messages` 用于放入 user / assistant 对话历史；`system` 是顶层字段，用于放入 system 指令；`max_tokens` 是必填字段，用于限制模型最多生成的 token 数。调用 Anthropic 官方 API 时，需要使用 `x-api-key` 请求头，并且需要传 `anthropic-version`，常用版本是 `2023-06-01`。

Anthropic Messages API 开启流式输出时，需要在请求体中设置 `stream = true`，服务端会通过 SSE 返回一系列命名事件。真正的文本增量通常在 `content_block_delta` 事件的 `delta.text` 字段里。

这个示例只使用 `WebClient` 发起请求，不需要通过 Spring Boot 启动项目。

## maven 依赖

```xml
<dependencies>
    <!-- WebClient 依赖-->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-webflux</artifactId>
        <version>3.5.14</version>
    </dependency>
    <!-- 解决 MacOS 下 netty 报错-->
    <dependency>
        <groupId>io.netty</groupId>
        <artifactId>netty-resolver-dns-native-macos</artifactId>
        <version>4.1.132.Final</version>
        <classifier>osx-aarch_64</classifier>
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.13.0</version>
            <configuration>
                <source>25</source>
                <target>25</target>
            </configuration>
        </plugin>
    </plugins>
</build>
```

## 代码

### 统一的 LLM 消息对象

```java
package com.example.dto;

/**
 * 统一的 LLM 消息对象，用于表示一条对话消息。
 */
public record LlmMessage(
        String role, // 消息角色
        String content // 消息内容
) {
    // 创建 user 消息，用于表示用户输入。
    public static LlmMessage user(String content) {
        return new LlmMessage("user", content);
    }

    // 创建 assistant 消息，用于表示模型历史回复。
    public static LlmMessage assistant(String content) {
        return new LlmMessage("assistant", content);
    }
}
```

### Anthropic Messages API 请求体

```java
package com.example.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

/**
 * Anthropic Messages API 请求体。
 * system 是顶层字段，不放在 messages 数组里。
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
public record AnthropicMessagesRequest(
        String model, // 要调用的 Claude 模型名称
        String system, // system 指令
        List<LlmMessage> messages, // 对话消息列表
        @JsonProperty("max_tokens") Integer maxTokens, // 限制模型最多生成多少 token
        Boolean stream // 是否启用流式输出
) {
}
```

### Anthropic Messages API 流式事件 DTO

```java
package com.example.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

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
```

### 请求大模型 API

```java
package com.example.demo;

import com.example.dto.AnthropicMessagesRequest;
import com.example.dto.AnthropicStreamEvent;
import com.example.dto.LlmMessage;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.util.List;

public class AnthropicMessagesStreamDemo {
    static void main() {
        // Jackson JSON 解析器，用于解析每个 SSE data 里的 JSON 字符串。
        ObjectMapper objectMapper = new ObjectMapper();

        // 构造 Messages API 流式请求体。
        AnthropicMessagesRequest request = new AnthropicMessagesRequest(
                "claude-sonnet-4-5", // 模型
                "你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。", // system
                List.of(
                        LlmMessage.user("用一句话解释什么是 RAG。")
                ),
                1000, // max_tokens
                true // 启用流式输出
        );

        String API_KEY = "换成你自己的KEY";

        WebClient webClient = WebClient.builder()
                .baseUrl("https://api.anthropic.com/v1")
                .defaultHeader("x-api-key", API_KEY)
                .defaultHeader("anthropic-version", "2023-06-01")
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();

        System.out.println("正在询问 AI...");
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
                        // message_stop 表示模型消息已经结束，WebClient 会在 HTTP 流结束后自然完成。
                        return;
                    }
                })
                .blockLast();

        // 流式输出结束后补一个换行。
        System.out.println();
    }
}
```
