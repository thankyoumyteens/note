# 给 OpenAiCompatibleLlmClient 增加条件注解

避免项目里同时存在两个 `LlmClient` Bean。

Spring 容器中如果同时有：

```text
OpenAiCompatibleLlmClient implements LlmClient
SpringAiLlmClient implements LlmClient
```

而 Service 构造器只注入：

```java
LlmClient llmClient
```

Spring 会不知道该注入哪个。

所以必须用条件注解控制：

```text
llm.provider=openai-compatible -> 使用 OpenAiCompatibleLlmClient
llm.provider=spring-ai -> 使用 SpringAiLlmClient
```

#### 代码

修改：

```text
src/main/java/com/example/aigateway/client/openai/OpenAiCompatibleLlmClient.java
```

在类上增加：

```java
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
```

然后把类注解改成：

```java
@Component
@ConditionalOnProperty(
        name = "llm.provider",
        havingValue = "openai-compatible",
        matchIfMissing = true
)
public class OpenAiCompatibleLlmClient implements LlmClient {
    // 原有代码不变
}
```

#### 代码说明

`matchIfMissing = true` 的意思是：

```text
如果没有配置 llm.provider，默认使用 openai-compatible
```

这样不会破坏你当前已经跑通的主线实现。
