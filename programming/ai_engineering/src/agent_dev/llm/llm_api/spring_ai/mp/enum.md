# Provider 枚举

```java
package com.example.ai;

/**
 * 支持的模型服务商。
 * 用枚举可以避免业务代码里到处写字符串。
 */
public enum LlmProvider {
    OPENAI,
    CLAUDE,
    QWEN
}
```
