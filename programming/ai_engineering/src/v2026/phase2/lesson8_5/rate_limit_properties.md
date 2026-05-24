# 新增 RateLimitProperties

文件：

```text
src/main/java/com/example/aigateway/config/RateLimitProperties.java
```

代码：

```java
package com.example.aigateway.config;

import com.example.aigateway.dto.LlmCallType;
import java.util.EnumMap;
import java.util.Map;
import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * AI Gateway 限流配置。
 *
 * 对应 application.yml:
 *
 * ai:
 *   rate-limit:
 *     enabled: true
 *     default-rule:
 *       limit: 60
 *       window-seconds: 60
 *     call-type-rules:
 *       CHAT:
 *         limit: 30
 *         window-seconds: 60
 */
@ConfigurationProperties(prefix = "ai.rate-limit")
public class RateLimitProperties {

    /**
     * 是否启用限流。
     * 本地调试时可以临时设置为 false。
     */
    private boolean enabled = true;

    /**
     * 默认限流规则。
     */
    private Rule defaultRule = new Rule(60, 60);

    /**
     * 按 LlmCallType 设置的限流规则。
     */
    private Map<LlmCallType, Rule> callTypeRules = new EnumMap<>(LlmCallType.class);

    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }

    public Rule getDefaultRule() {
        return defaultRule;
    }

    public void setDefaultRule(Rule defaultRule) {
        this.defaultRule = defaultRule;
    }

    public Map<LlmCallType, Rule> getCallTypeRules() {
        return callTypeRules;
    }

    public void setCallTypeRules(Map<LlmCallType, Rule> callTypeRules) {
        this.callTypeRules = callTypeRules;
    }

    /**
     * 单条限流规则。
     *
     * limit：窗口内最多允许多少次调用
     * windowSeconds：窗口长度，单位秒
     */
    public record Rule(
            int limit,
            int windowSeconds
    ) {
    }
}
```

`Rule` 表示一条限流规则：

```text
limit = 允许次数
windowSeconds = 时间窗口
```

例如：

```yaml
limit: 30
window-seconds: 60
```

意思是：

```text
60 秒内最多允许 30 次
```

## 启用 RateLimitProperties

只有写了 `@ConfigurationProperties` 还不够，还需要让 Spring Boot 知道要启用这个配置类。

#### 代码

修改启动类：

```text
src/main/java/com/example/aigateway/AiGatewayApplication.java
```

```java
package com.example.aigateway;

import com.example.aigateway.config.LlmProperties;
import com.example.aigateway.config.RateLimitProperties;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

/**
 * AI Gateway 启动类。
 */
@SpringBootApplication
@EnableConfigurationProperties({
        LlmProperties.class,
        RateLimitProperties.class
})
public class AiGatewayApplication {

    public static void main(String[] args) {
        SpringApplication.run(AiGatewayApplication.class, args);
    }
}
```
