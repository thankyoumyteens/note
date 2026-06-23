# 调用 Anthropic Messages API

Anthropic Messages API 使用 `POST /v1/messages` 创建模型响应；`messages` 用于放入 user / assistant 对话历史；`system` 是顶层字段，用于放入 system 指令；`max_tokens` 是必填字段，用于限制模型最多生成的 token 数。调用 Anthropic 官方 API 时，需要使用 `x-api-key` 请求头，并且需要传 `anthropic-version`，常用版本是 `2023-06-01`。

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

### Anthropic Messages API 响应体

```java
package com.example.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

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
```

### 请求大模型 API

```java
package com.example.demo;

import com.example.dto.*;
import org.apache.logging.log4j.message.Message;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.util.List;

public class AnthropicDemo {
    static void main() {
        // 构造 Messages API 请求体。
        AnthropicMessagesRequest request = new AnthropicMessagesRequest(
                "claude-sonnet-4-5", // 模型
                "你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。", // system
                List.of(
                        LlmMessage.user("用一句话解释什么是 RAG。")
                ),
                1000, // max_tokens
                false // 不使用流式输出
        );

        String API_KEY = "换成你自己的KEY";

        WebClient webClient = WebClient.builder()
                .baseUrl("https://api.anthropic.com/v1")
                .defaultHeader("x-api-key", API_KEY)
                .defaultHeader("anthropic-version", "2023-06-01")
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();
        System.out.println("正在询问 AI...");
        // 发送请求并把响应反序列化为 AnthropicMessagesResponse。
        AnthropicMessagesResponse response = webClient.post()
                .uri("/messages")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(AnthropicMessagesResponse.class)
                .timeout(Duration.ofSeconds(60))
                .block();

        if (response == null) {
            System.out.println("出错");
            return;
        }
        // 提取模型最终文本。
        String content = response.firstText();
        System.out.println("AI 回答：");
        System.out.println(content);
    }
}
```
