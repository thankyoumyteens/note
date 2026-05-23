# 新增 LlmCallType

## 为什么要记录 callType

当前你的模型调用已经有多种用途：

```text
普通聊天
结构化任务抽取
JSON 修复
工具调用决策
流式聊天
```

它们都调用模型，但业务含义不同。

所以需要 `LlmCallType`：

```text
CHAT
STREAM_CHAT
TASK_EXTRACTION
JSON_REPAIR
TOOL_DECISION
COMPLETE
```

这样后续可以统计：

```text
哪个调用类型最慢？
哪个调用类型最贵？
哪个调用类型最容易失败？
```

## 代码实现

文件：

```text
src/main/java/com/example/aigateway/dto/LlmCallType.java
```

```java
package com.example.aigateway.dto;

/**
 * 大模型调用类型。
 *
 * 作用：
 * - 区分不同业务场景下的模型调用
 * - 便于后续统计成本、延迟和失败率
 */
public enum LlmCallType {

    /**
     * 普通聊天。
     */
    CHAT,

    /**
     * 流式聊天。
     */
    STREAM_CHAT,

    /**
     * 通用模型调用。
     */
    COMPLETE,

    /**
     * 任务抽取。
     */
    TASK_EXTRACTION,

    /**
     * JSON 修复。
     */
    JSON_REPAIR,

    /**
     * 工具调用决策。
     */
    TOOL_DECISION
}
```
