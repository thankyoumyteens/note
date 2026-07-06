# Maven 依赖

由于你要手动创建多个 `ChatModel / ChatClient`，这里不使用 starter，改用底层模块。

```xml
<dependencies>
    <!-- Spring MVC Controller -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <!-- WebFlux / Reactor：Controller 返回 Flux<ServerSentEvent<...>> 需要 -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-webflux</artifactId>
    </dependency>

    <!-- Spring AI OpenAI / OpenAI-compatible 模块 -->
    <dependency>
        <groupId>org.springframework.ai</groupId>
        <artifactId>spring-ai-openai</artifactId>
    </dependency>

    <!-- Spring AI Anthropic 模块 -->
    <dependency>
        <groupId>org.springframework.ai</groupId>
        <artifactId>spring-ai-anthropic</artifactId>
    </dependency>

    <!-- Spring AI ChatClient -->
    <dependency>
        <groupId>org.springframework.ai</groupId>
        <artifactId>spring-ai-client-chat</artifactId>
    </dependency>

    <!-- 配置属性元数据，方便 IDE 自动补全 application.yml -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-configuration-processor</artifactId>
        <optional>true</optional>
    </dependency>
</dependencies>
```
