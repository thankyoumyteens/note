# 利用 LangChain 的自动重试解析器，让 AI 自动纠错重写

AI 工程化的现实问题：现在的代码在理想状态下跑得很顺畅，但现实中，大模型偶尔会产生幻觉（Hallucination）。比如，就算你千叮咛万嘱咐，它依然可能在输出的 JSON 外面包了一层 Markdown 的 `json ...` 代码块，或者少输出一个字段，直接导致 PydanticOutputParser 抛出异常崩溃。

在传统的 Java 开发中，遇到外部系统返回了格式错误的数据（比如少了一个字段，或者 JSON 格式错乱），标准的做法是：全局异常拦截（`@ControllerAdvice`），记录日志，然后给前端返回一个 500 Internal Server Error 或者业务错误码，让用户重试。或者，你会使用 Spring Retry（`@Retryable`）去重新发起一次相同的请求，祈祷下一次网络能返回正确的数据。

但在 AI 原生应用中，大模型具有“阅读报错并自我修复”的推理能力。当解析失败时，我们不需要直接向客户端抛出异常，而是可以把报错的堆栈信息和它刚才输出的错误内容一起丢回给它，命令它：“你刚才给我的 JSON 格式不对，这是报错信息，请你修复它。”

## 引入 AI 自动纠错机制

### 1. 安装依赖

```sh
pip install langchain-classic
```

### 2. 代码

```py
import os

import env_setup

import uvicorn
from fastapi import FastAPI, HTTPException
from langchain_classic.output_parsers import RetryWithErrorOutputParser
from langchain_core.exceptions import OutputParserException
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

app = FastAPI(title="AI Financial News Extractor (With Retry)")


class NewsRequest(BaseModel):
    content: str = Field(..., min_length=15, description="新闻文本内容")


class MarketNewsExtraction(BaseModel):
    company_name: str = Field(description="公司名称或股票代码，例如 Palantir (PLTR)")
    main_event: str = Field(description="新闻中的核心事件主体，简明扼要")
    financial_impact: str = Field(description="对公司财报、利润率或基本面的潜在影响分析")


model = ChatOpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
    model="Pro/moonshotai/Kimi-K2.5",
    temperature=0,
)

# 基础解析器
base_parser = PydanticOutputParser(pydantic_object=MarketNewsExtraction)

# 【新增】：初始化带错误反馈的重试解析器
# 它需要知道你期望的数据格式（base_parser）以及用来执行纠错任务的大模型（llm）
retry_parser = RetryWithErrorOutputParser.from_llm(
    parser=base_parser,
    llm=model
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system",
     "你是一个华尔街资深量化分析师的助手，负责从冗杂的市场新闻中提取精准的结构化数据。\n\n{format_instructions}"),
    ("user", "请提取以下新闻的关键信息：\n\n{news_text}")
])


# ==========================================
# 3. 定义 Controller 接口 (包含纠错逻辑)
# ==========================================
@app.post("/api/v1/extract-news", response_model=MarketNewsExtraction)
async def extract_news(request: NewsRequest):
    # 第一步：填充模板，生成 PromptValue 对象 (包含了完整上下文)
    prompt_value = await prompt_template.ainvoke({
        "news_text": request.content,
        "format_instructions": base_parser.get_format_instructions()
    })

    # 第二步：调用大模型，获取原始文本输出
    # 注意：这里我们剥离了 LCEL 中的 parser 环节，只让数据流到 model 层，以便拿到原始字符串
    llm_response = await model.ainvoke(prompt_value)

    try:
        # 第三步：尝试使用基础解析器将其转换为 Pydantic 对象
        # 相当于 Java 中的 JSON.parseObject()
        result = base_parser.parse(llm_response.content)
        return result

    except OutputParserException as e:
        # 第四步：【核心魔法】捕获解析异常，触发 AI 自我纠错！
        print(f"⚠️ 首次解析失败，大模型输出了非法格式！正在请求 AI 自我纠错...\n报错详情: {e}")

        try:
            # aparse_with_prompt 方法会将三个要素打包发给大模型：
            # 1. 原本的指令上下文 (prompt_value)
            # 2. 它刚才搞砸的错误回答 (llm_response.content)
            # 3. 具体的报错信息 (比如 "missing field 'company_name'")
            retry_result = await retry_parser.aparse_with_prompt(
                completion=llm_response.content,
                prompt_value=prompt_value
            )
            print("✅ AI 纠错成功，已恢复合法数据结构！")
            return retry_result

        except Exception as retry_e:
            # 如果重试后依然失败（极其罕见，除非大模型彻底崩溃或提示词极度冲突），才向前端抛出 500
            raise HTTPException(status_code=500, detail=f"AI 纠错后依然解析失败: {str(retry_e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
