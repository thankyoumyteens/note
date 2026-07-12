# 调用 OpenAI-compatible API

用 Spring 官方的 `WebClient` 处理 OpenAI-compatible API 的流式 HTTP 调用。

流式调用的核心变化是：

1. 请求体 `stream = true`
2. 响应类型从普通 JSON 变成 `text/event-stream`
3. 每个 SSE 事件里解析 `choices[].delta.content`
4. 遇到 `[DONE]` 表示流结束

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
```

### 适用于 OpenAI 风格的请求体 DTO

```java
package com.example.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

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
```

### 适用于 OpenAI 风格的流式响应体 DTO

```java
package com.example.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

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
     */
    @JsonIgnoreProperties(ignoreUnknown = true)
    public record Delta(
            String role, // role 通常是 assistant，且一般只在第一个 chunk 出现
            String content // 当前增量文本
    ) {
    }
}
```

### 请求大模型 API

```java
package com.example.demo;

import com.example.dto.LlmMessage;
import com.example.dto.OpenAiChatRequest;
import com.example.dto.OpenAiChatStreamResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.util.List;

public class OpenAiCompatibleStreamDemo {
    static void main() {
        // Jackson JSON 解析器，用于解析每个 SSE data 里的 JSON 字符串。
        ObjectMapper objectMapper = new ObjectMapper();

        // 要发给大模型的消息。
        List<LlmMessage> messages = List.of(
                LlmMessage.system("你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。"),
                LlmMessage.user("用一句话解释什么是 RAG。")
        );

        OpenAiChatRequest request = new OpenAiChatRequest(
                "deepseek-v4-pro", // 模型
                messages, // 对话列表
                0.2, // temperature
                1000, // max_tokens
                true // 启用流式输出
        );

        String API_KEY = "换成你自己的KEY";

        WebClient webClient = WebClient.builder()
                // 以 DeepSeek 为例。
                .baseUrl("https://api.deepseek.com")
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + API_KEY)
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();

        System.out.println("正在询问 AI...");
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
