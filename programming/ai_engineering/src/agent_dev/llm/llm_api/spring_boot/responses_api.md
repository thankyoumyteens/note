# 调用 OpenAI Responses API

Responses API 使用 `POST /v1/responses` 创建模型响应；`input` 可以直接传字符串，等价于 user 文本输入；`instructions` 用于放入 system/developer 类指令；`max_output_tokens` 用于限制模型最多生成的 token 数。

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

### Responses API 响应体

```java
package com.example.dto;

import java.util.List;

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
```

### 请求大模型 API

```java
package com.example.demo;

import com.example.dto.*;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.util.List;

public class OpenAiResponseApiDemo {
    static void main() {
        // 构造 Responses API 请求体。
        OpenAiResponsesRequest request = new OpenAiResponsesRequest(
                System.getenv("LLM_MODEL"), // 模型
                "你是一个严谨、清晰的 Java 后端和 AI Agent 开发助手。", // instructions
                "用一句话解释什么是 RAG。", // input
                0.2, // temperature
                1000, // max_output_tokens
                false // 不使用流式输出
        );

        String apiKey = System.getenv("LLM_API_KEY");
        String baseUrl = System.getenv().getOrDefault(
                "LLM_BASE_URL",
                "https://api.openai.com/v1"
        );

        WebClient webClient = WebClient.builder()
                .baseUrl(baseUrl)
                .defaultHeader(HttpHeaders.AUTHORIZATION, "Bearer " + apiKey)
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();
        System.out.println("正在询问 AI...");
        // 发送请求并把响应反序列化为 OpenAiResponsesResponse。
        OpenAiResponsesResponse response = webClient.post()
                .uri("/responses")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(OpenAiResponsesResponse.class)
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
