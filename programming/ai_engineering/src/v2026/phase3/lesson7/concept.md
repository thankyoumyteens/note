# 核心概念

## 什么是 token？

Token 是大模型处理文本的基本单位。

可以粗略理解为：

```text
英文：一个单词可能是 1 个或多个 token
中文：一个字或一个词可能是 1 个或多个 token
```

模型调用一般会返回 usage：

```json
{
  "usage": {
    "prompt_tokens": 120,
    "completion_tokens": 80,
    "total_tokens": 200
  }
}
```

含义：

| 字段                | 含义           |
| ------------------- | -------------- |
| `prompt_tokens`     | 输入消耗 token |
| `completion_tokens` | 输出消耗 token |
| `total_tokens`      | 总 token       |

成本统计通常基于这些字段。
