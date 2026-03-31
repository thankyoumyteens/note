# 核心防线一：Prompt 模板的“沙盒隔离” (Context Isolation)

在朴素 RAG 中，最危险的做法就是直接把检索到的文本和用户的问题用字符串拼接（String Concatenation）在一起。这就像是在 Java 里直接拼接sql一样致命：

```sql
String sql = "SELECT * FROM users WHERE name = '" + userInput + "'";
```

现代 LLM（尤其是 Claude、Qwen 和 DeepSeek）在预训练时，阅读了海量的 HTML 和 XML 代码。因此，XML 标签（XML Tags） 是目前业界公认最好的“隔离沙盒”。

❌ 业余的做法（字符串裸奔）：

```
结合以下参考资料回答问题。
参考资料：{context}
用户问题：{question}
```

✅ 架构师的做法（XML 严格界定）：

```xml
你是一个专业的投研助手。请严格且仅根据 <context> 标签内的参考资料来回答 <user_query> 标签内的问题。

<context>
{context}
</context>

<user_query>
{question}
</user_query>
```

通过 XML 标签，大模型能极其清晰地感知到：`<context>` 里面的东西是“只读数据（Data）”，绝不是我要执行的“指令（Instruction）”。
