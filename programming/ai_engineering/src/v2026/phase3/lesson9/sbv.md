# 升级 Spring Boot 版本并引入 Spring AI

`pom.xml` 中原来可能是：

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.4</version>
</parent>
```

建议改成一个 Spring AI 支持范围内的版本，例如：

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.5.14</version>
</parent>
```

版本号你可以按自己环境选择 3.4.x 或 3.5.x。官方 Getting Started 当前说明 Spring AI 支持 Spring Boot 3.4.x 和 3.5.x。

**注意：如果有类似下面的配置也需要同步修改**

```xml
<properties>
    <spring-boot.version>3.2.4</spring-boot.version>
</properties>
```

## 5.2 引入 Spring AI BOM

Spring AI 官方文档建议使用 BOM 管理 Spring AI 依赖版本，保证项目中 Spring AI 组件版本一致。

在 `pom.xml` 增加：

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.ai</groupId>
            <artifactId>spring-ai-bom</artifactId>
            <version>1.1.6</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

如果你使用的是 Spring AI 1.0.x，可以把版本改为对应版本。
不要混用多个 Spring AI 版本。

## 引入 OpenAI Starter

官方 OpenAI Chat 文档当前使用的 starter 是：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-openai</artifactId>
</dependency>
```

Spring AI 文档也提示 starter artifact 名称有过较大变化，因此不要沿用很老教程里的 `spring-ai-openai-spring-boot-starter`。

加入：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-openai</artifactId>
</dependency>
```
