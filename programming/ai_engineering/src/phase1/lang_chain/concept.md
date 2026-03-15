# 核心概念

## ChatPromptTemplate：告别丑陋的字符串拼接

在原生 SDK 中，我们要自己维护一个包含 dict 的 list (`[{"role": "user", "content": "..."}]`)。如果内容里有变量，还要用到 Python 的 f-string。

ChatPromptTemplate 帮我们将提示词与变量解耦。你只需要定义好“占位符”，它会在执行时自动将变量填入，生成标准的消息格式。

## OutputParsers (与 Pydantic)：大模型的“反序列化器”

大模型本质上是一个“文本接龙”机器，它吐出的永远是字符串 (String)。但是在代码里，我们需要的是对象 (Object)。
Pydantic 是 Python 里定义数据结构的标杆（类似于 Java 的 POJO/Record 加上了 JSR 380 校验注解）。OutputParser 的作用就是：

1. 自动生成一段 Prompt，告诉大模型“请按照这个 JSON 格式输出”。
2. 拿到大模型的文本结果后，自动解析（反序列化）成你定义好的 Pydantic 对象。

## LCEL (LangChain 表达式语言)：优雅的 Unix 管道

如果你熟悉 Linux 的 `cat data.txt | grep "error" | awk '{print $1}'`，或者 Java 8 的 Stream API，LCEL 你就能秒懂。

它通过重载 Python 的按位或运算符 `|`，把多个组件串联起来：

```py
chain = prompt | model | parser
```

数据就像流水一样：字典输入 -> 填入 Prompt -> 变成消息传给 Model -> 生成文本传给 Parser -> 变成 Python 对象输出。
