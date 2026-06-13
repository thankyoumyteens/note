# Maven 基础依赖

Spring AI 推荐通过 BOM 管理版本。

注意：Spring AI 1.1.x 对应 Spring Boot 3.5.x。

```xml
<properties>
    <spring-boot.version>3.5.14</spring-boot.version>
    <spring-ai.version>1.1.6</spring-ai.version>
</properties>

<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>${spring-boot.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
        <!-- 统一管理 Spring AI 相关依赖版本，避免各模块版本不一致。 -->
        <dependency>
            <groupId>org.springframework.ai</groupId>
            <artifactId>spring-ai-bom</artifactId>
            <version>${spring-ai.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

普通 Web 项目：

```xml
<dependencies>
    <!-- 提供 Controller、REST API 等 Spring Boot Web 能力。 -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <!-- Spring AI 的 OpenAI 模型接入 starter。 -->
    <dependency>
        <groupId>org.springframework.ai</groupId>
        <artifactId>spring-ai-starter-model-openai</artifactId>
    </dependency>
</dependencies>
```

如果要接 Claude，再加：

```xml
<!-- Spring AI 的 Anthropic / Claude 模型接入 starter。 -->
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-anthropic</artifactId>
</dependency>
```

如果要接 DeepSeek 原生 starter，再加：

```xml
<!-- Spring AI 的 DeepSeek 模型接入 starter。 -->
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-deepseek</artifactId>
</dependency>
```
