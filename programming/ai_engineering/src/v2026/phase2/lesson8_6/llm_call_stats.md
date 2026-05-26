# 新增 LlmCallStats

提供一个基础统计接口的响应 DTO。

统计接口应该返回结构化数据，而不是字符串。

#### 代码

文件：

```text
src/main/java/com/example/aigateway/dto/LlmCallStats.java
```

代码：

```java
package com.example.aigateway.dto;

/**
 * 模型调用基础统计。
 *
 * 当前统计最近 100 条日志。
 */
public record LlmCallStats(
        long total,
        long success,
        long failure,
        double avgLatencyMs,
        long totalTokens
) {
}
```

#### 代码说明

字段含义：

```text
total：统计样本数
success：成功数
failure：失败数
avgLatencyMs：平均延迟
totalTokens：总 token 消耗
```
