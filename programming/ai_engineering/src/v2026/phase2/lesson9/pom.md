# 引入 Spring AI BOM 和 OpenAI Starter

让项目具备 Spring AI 的 ChatClient 能力。

BOM 用来统一 Spring AI 相关依赖版本，避免每个依赖都手动写版本。

Spring AI 官方说明它提供 Spring Boot Auto Configuration 和 Starters；Spring AI 项目页也说明 ChatClient 是一个类似 WebClient / RestClient 风格的 Fluent API。

#### 代码

在 `pom.xml` 增加属性：

```xml
<properties>
    <spring-ai.version>1.1.0</spring-ai.version>
</properties>
```

增加 dependency management：

```xml
<dependencyManagement>
    <dependencies>
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

增加依赖：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-openai</artifactId>
</dependency>
```
