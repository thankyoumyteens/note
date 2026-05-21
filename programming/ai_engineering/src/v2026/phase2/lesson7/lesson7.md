# 第 7 课：Evals 优先：结构化输出与工具调用评估

前面第 4、5、6 课已经实现了：

```text
/api/ai/extract-task
/api/ai/order-assistant
```

但现在有一个新问题：

```text
接口能跑通，不代表效果稳定。
```

例如：

```text
同一个 Prompt，换几个输入后是否还稳定？
模型是否经常把 priority 抽错？
模型是否会漏掉 orderId？
模型是否会对非订单问题乱调用工具？
Prompt 改了一行后，效果是变好还是变差？
```

一句话概括：

> 本课建立 evals 目录、golden dataset 和 Python 评估脚本，用数据衡量结构化输出和工具调用效果。

本课不会改 Java 主服务核心逻辑，只增加：

```text
evals/
```
