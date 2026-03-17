# 用 LangChain 搭建朴素 RAG

我们用 Python + LangChain + Chroma（本地轻量级向量库）+ OpenAI API 来跑通这六步。

### 1. 安装依赖

```py
pip install langchain langchain-openai langchain-chroma chromadb tiktoken
```

### 2. 代码实现（请仔细看注释里的 1~6 步对应关系）
