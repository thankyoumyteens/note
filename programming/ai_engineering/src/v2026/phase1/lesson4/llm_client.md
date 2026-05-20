# 扩展 LlmClient

文件：

```text
src/main/java/com/example/aigateway/client/LlmClient.java
```

修改为：

```java
package com.example.aigateway.client;

import reactor.core.publisher.Flux;

/**
 * 大模型调用统一抽象。
 *
 * 所有业务代码都应该依赖 LlmClient，
 * 而不是直接依赖具体模型供应商。
 */
public interface LlmClient {

    /**
     * 普通聊天：等待模型完整生成后，一次性返回完整字符串。
     */
    String chat(String message);

    /**
     * 流式聊天：模型边生成边返回多个文本片段。
     */
    Flux<String> streamChat(String message);

    /**
     * 通用模型调用方法。
     *
     * systemPrompt：定义模型在本次任务中的角色和规则。
     * userPrompt：用户输入或待处理文本。
     *
     * 后续结构化输出、JSON 修复、工具调用决策都可以复用该方法。
     */
    String complete(String systemPrompt, String userPrompt);
}
```
