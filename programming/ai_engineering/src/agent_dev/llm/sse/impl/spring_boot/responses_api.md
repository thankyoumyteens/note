# 调用 OpenAI Responses API

Responses API 使用 `POST /v1/responses` 创建模型响应；`input` 可以直接传字符串，等价于 user 文本输入；`instructions` 用于放入 system/developer 类指令；`max_output_tokens` 用于限制模型最多生成的 token 数。

Responses API 的流式输出不是一次性返回完整 `output[].content[].text`，而是返回一组 SSE 事件。真正的增量文本在 `response.output_text.delta` 事件的 `delta` 字段里。

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

### Responses API 请求体

```java
package com.example.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

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
```

### Responses API 流式事件 DTO

```java
package com.example.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * Responses API 流式事件。
 *
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
```

### 请求大模型 API

```java
package com.example.demo;

import com.example.dto.OpenAiResponsesRequest;
import com.example.dto.OpenAiResponsesStreamEvent;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;

public class OpenAiResponsesStreamDemo {
    static void main() {
        // Jackson JSON 解析器，用于解析每个 SSE data 里的 JSON 字符串。
        ObjectMapper objectMapper = new ObjectMapper();

        // 构造 Responses API 流式请求体。
        OpenAiResponsesRequest request = new OpenAiResponsesRequest(
                "gpt-4o-mini", // 模型
                "你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。", // instructions
                "用一句话解释什么是 RAG。", // input
                0.2, // temperature
                1000, // max_output_tokens
                true // 启用流式输出
        );

        String API_KEY = "换成你自己的KEY";

        WebClient webClient = WebClient.builder()
                .baseUrl("https://api.openai.com/v1")
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + API_KEY)
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();

        System.out.println("正在询问 AI...");
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
