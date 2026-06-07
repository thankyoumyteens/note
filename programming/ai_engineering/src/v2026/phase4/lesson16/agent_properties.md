# 新增 AgentProperties

限制 Agent 最多执行多少步，防止陷入循环。

Agent 最大风险之一是：

```text
模型不断思考、不断调用工具、不断重试
```

所以必须有：

```text
maxSteps
```

### 代码

文件：

```text
src/main/java/com/example/aigateway/agent/config/AgentProperties.java
```

```java
package com.example.aigateway.agent.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * Agent Workflow 配置。
 *
 * 第 16 课重点：
 * - 不允许无限循环
 * - 每个 workflow 最多执行 maxSteps 步
 */
@ConfigurationProperties(prefix = "ai.agent")
public class AgentProperties {

    /**
     * 单个 Agent workflow 最多执行多少步。
     */
    private int maxSteps = 6;

    public int getMaxSteps() {
        return maxSteps;
    }

    public void setMaxSteps(int maxSteps) {
        this.maxSteps = maxSteps;
    }
}
```

`application.yml` 增加：

```yaml
ai:
  agent:
    max-steps: 6
```

启动类启用：

```java
@EnableConfigurationProperties({
        LlmProperties.class,
        RateLimitProperties.class,
        EmbeddingProperties.class,
        RagProperties.class,
        ContextProperties.class,
        AgentProperties.class
})
```

### 代码说明

`maxSteps = 6` 表示一个工单最多执行 6 个 Agent step。
