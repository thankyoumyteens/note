# 新增 ToolProperties

限制单个 Agent workflow 最多能调用多少次工具，防止工具调用失控。

第 16 课限制的是：

```text
agent step 次数
```

第 17 课限制的是：

```text
tool 调用次数
```

这两个不是一回事。

一个 step 里理论上可能调用多个工具，所以工具调用也需要单独限流。

### 代码

文件：

```text
src/main/java/com/example/aigateway/tool/config/ToolProperties.java
```

```java
package com.example.aigateway.tool.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * 工具调用配置。
 *
 * 第 17 课重点：
 * - 限制单个 workflow 内的工具调用次数
 * - 防止 Agent 反复调用工具造成成本、风险和副作用失控
 */
@ConfigurationProperties(prefix = "ai.tool")
public class ToolProperties {

    /**
     * 单个 Agent workflow 最多允许调用多少次工具。
     */
    private int maxToolCallsPerWorkflow = 5;

    public int getMaxToolCallsPerWorkflow() {
        return maxToolCallsPerWorkflow;
    }

    public void setMaxToolCallsPerWorkflow(int maxToolCallsPerWorkflow) {
        this.maxToolCallsPerWorkflow = maxToolCallsPerWorkflow;
    }
}
```

`application.yml` 增加：

```yaml
ai:
  tool:
    max-tool-calls-per-workflow: 5
```

启动类启用：

```java
@EnableConfigurationProperties({
        LlmProperties.class,
        RateLimitProperties.class,
        EmbeddingProperties.class,
        RagProperties.class,
        ContextProperties.class,
        AgentProperties.class,
        ToolProperties.class
})
```

### 代码说明

第 17 课只做 workflow 内的简单工具调用限制，不做全局 Redis 限流。

全局 tool quota 后续可以放到第 20 课 LLMOps 统一治理。
