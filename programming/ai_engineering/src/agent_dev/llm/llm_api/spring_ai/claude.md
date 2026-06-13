# 调用 Claude

Claude 用 Anthropic starter。

## Maven

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-anthropic</artifactId>
</dependency>
```

## application.yml

```yaml
spring:
  ai:
    model:
      chat: anthropic

    anthropic:
      api-key: ${ANTHROPIC_API_KEY}
      chat:
        options:
          model: claude-haiku-4-5
          max-tokens: 4096
          temperature: 0.2
```

启动前设置：

```bash
export ANTHROPIC_API_KEY="你的 Anthropic API Key"
```

你的业务代码仍然是：

```java
return chatClient.prompt()
        .user(message)
        .call()
        .content();
```

不需要改成 Anthropic SDK 写法。
