# LLM 的基本工作流程

一个 LLM 从输入到输出，大致经过这些步骤：

1. 用户输入
2. 文本切成 token
3. token 转成向量
4. Transformer 处理上下文关系
5. 输出下一个 token 的概率分布
6. 选择一个 token
7. 继续预测下一个 token
8. 直到生成完整回答

LLM 不是一次性吐出完整答案，而是一个 token 一个 token 地生成。

## Token 是什么

Token 可以粗略理解成模型处理文本的最小单位。

英文里，一个 token 可能是：

- word
- subword
- punctuation

中文里，一个 token 可能是：

- 一个字
- 一个词的一部分
- 一个标点

例如：

```text
Spring Boot is powerful.
```

可能被切成：

```text
["Spring", " Boot", " is", " powerful", "."]
```

中文：

```text
大语言模型很强
```

可能被切成：

```text
["大", "语言", "模型", "很", "强"]
```

这就是为什么 LLM 会有：

- 上下文窗口
- token 限制
- 输入越长成本越高
- 输出越长越慢

因为模型处理的不是“字数”，而是 token 数。

## Embedding 是什么

Token 本身只是文本片段，模型不能直接理解文字。

所以每个 token 会被转换成一个向量，也就是一组数字。

比如：

- "Java" 被转换成 `[0.12, -0.44, 0.89, ...]`
- "Python" 被转换成 `[0.18, -0.39, 0.77, ...]`
- "Spring" 被转换成 `[0.21, -0.52, 0.91, ...]`

这个向量会表达 token 的语义、语法、上下文关系。

如果两个词经常出现在相似语境中，它们的向量距离就可能比较接近。

例如：Java、Spring Boot、后端开发、REST API、微服务，这些概念在向量空间里可能更接近。

这就是 Embedding 的基本思想。

在 RAG 里，Embedding 也很重要：

1. 文档 -> 切片 -> Embedding 转换成向量 -> 存入向量数据库
2. 用户问题 -> Embedding -> 向量检索 -> 找相似文档

## Transformer 是什么

现代 LLM 基本都基于 Transformer 架构。

你不需要从数学上完全掌握 Transformer，但需要知道它解决了一个核心问题：

> 如何让模型在生成当前 token 时，理解前面上下文中哪些内容最重要。

Transformer 的核心机制是：Self-Attention (自注意力机制)。它会判断：当前这个词应该关注前文里的哪些词？

比如句子：用户把订单取消了，因为它已经超时。

模型需要判断：“它”指的是订单，不是用户。

Attention 会帮助模型计算上下文中各个 token 之间的关联。

在代码场景里也是一样：

```java
public User getUserById(Long id) {
    return userRepository.findById(id);
}
```

模型需要知道：

- id 和 findById(id) 有关系
- User 和 userRepository 有关系
- 方法名 getUserById 和整体逻辑有关系

这类上下文关系，就是 Transformer 擅长处理的。
