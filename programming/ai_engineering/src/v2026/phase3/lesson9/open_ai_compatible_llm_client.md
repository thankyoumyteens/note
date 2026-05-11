# 修改 OpenAiCompatibleLlmClient

在 `OpenAiCompatibleLlmClient` 类上增加：

```java
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
```

然后改成：

```java
@Component
@ConditionalOnProperty(
        name = "llm.provider",
        havingValue = "openai-compatible",
        matchIfMissing = true
)
public class OpenAiCompatibleLlmClient implements LlmClient {
    ...
}
```

含义：

```text
llm.provider=openai-compatible 时启用
如果没配置，也默认启用
```
