# 调用 OpenAI-compatible API

用 Spring 官方的 `WebClient` 处理 HTTP 调用。

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

### 适用于 OpenAI 风格的响应体 DTO

```java
package com.example.dto;

import java.util.List;

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
        LlmMessage message = choices.getFirst().message();
        // message 或 content 为空时返回空字符串，保证调用方拿到稳定的 String。
        return message == null || message.content() == null ? "" : message.content();
    }

    /**
     * 单个候选结果。
     */
    public record Choice(
            LlmMessage message // 当前只关心其中的 message 字段
    ) {
    }
}
```

### 请求大模型 API

```java
package com.example.demo;

import com.example.dto.LlmMessage;
import com.example.dto.OpenAiChatRequest;
import com.example.dto.OpenAiChatResponse;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.util.List;

public class OpenAiDemo {
    static void main() {
        // 要发给大模型的消息
        List<LlmMessage> messages = List.of(
                LlmMessage.system("你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。"),
                LlmMessage.user("用一句话解释什么是泛型")
        );
        OpenAiChatRequest request = new OpenAiChatRequest(
                System.getenv("LLM_MODEL"), // 模型
                messages, // 对话列表
                0.2, // temperature
                1000, // max_tokens
                false // 不使用流式输出
        );

        String apiKey = System.getenv("LLM_API_KEY");
        String baseUrl = System.getenv().getOrDefault(
                "LLM_BASE_URL",
                "https://api.deepseek.com"
        );

        WebClient webClient = WebClient.builder()
                // 以 DeepSeek 为例
                .baseUrl(baseUrl)
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + apiKey)
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();
        System.out.println("正在询问 AI...");
        // 发送请求并把响应反序列化为 OpenAiChatResponse。
        OpenAiChatResponse response = webClient.post()
                .uri("/chat/completions")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(OpenAiChatResponse.class)
                .timeout(Duration.ofSeconds(60))
                .block();

        if (response == null) {
            System.out.println("出错");
            return;
        }
        // 提取第一个候选回答的文本内容。
        String content = response.firstText();
        System.out.println("AI 回答：");
        System.out.println(content);
    }
}
```
