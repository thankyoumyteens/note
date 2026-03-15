# 整合到 FastAPI

### 1. 安装依赖

```sh
pip install fastapi uvicorn langchain langchain-openai pydantic
```

### 2. main.py

```py
import os

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# ================= 豆包 (Volcengine) 配置区 =================
DOUBAO_API_KEY = os.environ.get("OPENAI_API_KEY")
DOUBAO_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
LLM_ENDPOINT_ID = os.environ.get("ENDPOINT_ID")  # 对话模型接入点id
# =========================================================

app = FastAPI(
    title="AI Financial News Extractor",
    description="将非结构化市场新闻转化为结构化数据的 API",
    version="1.0.0"
)


# ==========================================
# 1. 定义 DTO (数据传输对象)
# ==========================================

# 客户端请求的 JSON 结构 (FastAPI 会自动执行基础校验)
class NewsRequest(BaseModel):
    # ...放在 Field 的第一个参数位置（也就是 default 参数的位置）时，
    # 它的明确含义是：这个字段是必填项（Required），没有默认值
    content: str = Field(..., min_length=15, description="新闻文本内容，太短的内容没有提取价值")


# API 的返回结构，同时也是 AI 管道的解析目标
class MarketNewsExtraction(BaseModel):
    company_name: str = Field(description="公司名称或股票代码，例如 Palantir (PLTR)")
    main_event: str = Field(description="新闻中的核心事件主体，简明扼要")
    financial_impact: str = Field(description="对公司财报、利润率或基本面的潜在影响分析")


# ==========================================
# 2. 初始化 AI 组件 (类似 Spring 里的 @Bean，全局单例)
# ==========================================

parser = PydanticOutputParser(pydantic_object=MarketNewsExtraction)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "你是一个华尔街资深量化分析师的助手，负责从冗杂的市场新闻中提取精准的结构化数据。\n\n{format_instructions}"),
    ("user", "请提取以下新闻的关键信息：\n\n{news_text}")
])

model = ChatOpenAI(
    api_key=DOUBAO_API_KEY,
    base_url=DOUBAO_BASE_URL,
    model=LLM_ENDPOINT_ID,
    temperature=0,
)

# 组装 LCEL 管道
chain = prompt | model | parser


# ==========================================
# 3. 定义 Controller 接口
# ==========================================

@app.post("/api/v1/extract-news", response_model=MarketNewsExtraction)
async def extract_news(request: NewsRequest):
    """
    接收市场新闻文本，使用大模型提取关键信息并返回结构化 JSON。
    """
    try:
        # 【关键点】这里使用了 ainvoke (异步调用) 而不是 invoke
        # 因为调用大模型是典型的网络 I/O 密集型操作，异步可以释放主线程，大幅提升 API 并发能力
        result = await chain.ainvoke({
            "news_text": request.content,
            "format_instructions": parser.get_format_instructions()
        })
        return result

    except Exception as e:
        # 如果大模型抽风输出了非法的 JSON 导致 parser 解析失败，会在这里捕获
        raise HTTPException(status_code=500, detail=f"AI 解析失败: {str(e)}")


# ==========================================
# 4. 启动服务
# ==========================================
if __name__ == "__main__":
    # 在终端运行: python main.py
    # 或者: uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

async 和 await 的威力：当你调用 OpenAI(或其它大模型) 的 API 时，网络延迟可能长达 1-2 秒。在传统的同步阻塞模型中，这会卡死当前线程。Python 原生的 async/await 类似于 Java 的虚拟线程（Virtual Threads）或 WebFlux。当你的代码 `await chain.ainvoke(...)` 时，FastAPI 会把当前线程让出来去处理其他用户的 HTTP 请求，等 OpenAI 返回结果了再切回来继续执行。这对高并发的 AI 应用至关重要。
