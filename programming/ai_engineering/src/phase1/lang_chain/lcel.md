# 使用 LCEL 重写“信息抽取”任务

### 1. 安装依赖

```sh
pip install langchain langchain-openai pydantic
```

### 2. main.py

```py
import os

import env_setup

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser


# 1. 定义数据结构
class MarketNewsExtraction(BaseModel):
    company_name: str = Field(description="公司名称或股票代码，例如 Palantir (PLTR)")
    main_event: str = Field(description="新闻中的核心事件主体，简明扼要")
    financial_impact: str = Field(description="对公司财报、利润率或基本面的潜在影响分析")


# 2. 初始化解析器 (Parser)
# 它的作用有两个：生成一段让大模型输出 JSON 的指令；把大模型输出的 JSON 字符串反序列化为 Pydantic 对象
parser = PydanticOutputParser(pydantic_object=MarketNewsExtraction)

# 3. 构造 Prompt 模板 (ChatPromptTemplate)
# 注意这里的占位符 {format_instructions} 和 {news_text}
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "你是一个华尔街资深量化分析师的助手，负责从冗杂的市场新闻中提取精准的结构化数据。\n\n{format_instructions}"),
    ("user", "请提取以下新闻的关键信息：\n\n{news_text}")
])

# 4. 初始化大模型实例
model = ChatOpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
    model="Pro/moonshotai/Kimi-K2.5",
    # 抽取任务不需要模型有太多“创造力”，temperature 设为 0 保证输出的稳定性和一致性
    temperature=0,
)

# 5. 见证奇迹的时刻：LCEL 管道组装
# 这就像 Unix 的管道符 `|`，或者 Java Stream 的 `.map().filter()` 链式调用
chain = prompt | model | parser

# 模拟输入一段 PLTR 的杂乱新闻
sample_news = """
Palantir Technologies (PLTR) today announced a new $50 million contract with the Department of Defense
to expand its AIP (Artificial Intelligence Platform) integration. Analysts expect this to significantly
boost the company's Q3 revenue margins, though operating costs may slightly increase due to deployment scaling.
"""

# 6. 运行管道
# 执行调用：将变量传入管道，以替换掉占位符 {news_text} 和 {format_instructions}
result = chain.invoke({
    "news_text": sample_news,
    "format_instructions": parser.get_format_instructions()
})

# 7. 验证结果
print(f"返回结果类型: {type(result)}")
print("-" * 40)
print(f"公司名称: {result.company_name}")
print(f"核心事件: {result.main_event}")
print(f"财报影响: {result.financial_impact}")
```

## PydanticOutputParser 的魔法

你不需要自己在 Prompt 里苦口婆心地教大模型怎么写 JSON（比如“请严格输出大括号，不要加 markdown 标记...”）。

`parser.get_format_instructions()` 会根据你的 Pydantic 模型自动生成一套完美严苛的指令，塞进 System Prompt 里。

## `chain = prompt | model | parser` 是如何工作的？

在 Python 中，LangChain 重载了 `|` 运算符（通过 `__or__` 魔术方法）。

- 调用 `chain.invoke()` 时传入的数据首先作为 dict 流入 prompt，替换掉占位符，生成格式化的消息列表（List of Messages）。
- 这些消息自动流入 model，大模型进行推理，输出包含 JSON 文本的 AIMessage 对象。
- 这个 AIMessage 对象的文本内容最后流入 parser，被自动 `json.loads` 并转化为你定义的 MarketNewsExtraction 对象。
