# FastAPI + LangChain 流式接口

```py
import json
import os

import env_setup

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI(title="AI Financial Assistant (Streaming)")


class ChatRequest(BaseModel):
    session_id: str = Field(..., description="会话唯一标识")
    message: str = Field(..., description="用户当前的问题")


# ==========================================
# 初始化 AI 管道组件
# ==========================================
# 注意：流式输出不需要在 ChatOpenAI 里做特殊配置
model = ChatOpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
    model="Pro/moonshotai/Kimi-K2.5",
    temperature=0.7,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的华尔街金融顾问"),
    ("user", "{question}")
])

chain = prompt | model


# ==========================================
# 流式 Controller 接口
# ==========================================
@app.post("/api/v1/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    接收用户问题，以 Server-Sent Events (SSE) 格式流式返回 AI 的回答。
    """

    # 定义一个异步生成器函数
    async def generate_stream():
        # 【关键点】使用 .astream() 而不是 .ainvoke()
        # 它会返回一个异步迭代器，随着大模型的推理，一块一块地输出 (chunk)
        async for chunk in chain.astream(
                {"question": request.message},
                config={
                    "configurable": {"session_id": request.session_id}
                }
        ):
            # chunk.content 就是这一次吐出来的几个字符
            if chunk.content:
                # 按照标准的 SSE (Server-Sent Events) 格式拼接字符串
                # 格式必须是: data: {你的数据}\n\n
                # 为了防止换行符等特殊字符破坏协议，通常把内容包装成 JSON 字符串
                payload = json.dumps({"content": chunk.content}, ensure_ascii=False)
                yield f"data: {payload}\n\n"

        # 约定一个结束信号（可选，前端可以通过监听这个信号主动断开连接）
        yield "data: [DONE]\n\n"

    # 使用 FastAPI 的 StreamingResponse 包装生成器，并指定媒体类型为 event-stream
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream"
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

1. `async for chunk in ... astream()`：
   - 当大模型开始思考时，它不会等整段话说完。比如你问它“博格公式是什么”，它可能先输出“博”，再输出“格公”，再输出“式”。.`astream()` 能够实时捕获这些碎块（Chunks）。
2. yield 关键字：
   - 在 generate_stream 函数里，我们没有用 return。在 Python 中，包含了 yield 的函数就是一个生成器（Generator）。FastAPI 拿到这个生成器后，会保持 HTTP 连接不断开，每次 yield 吐出一个字符串，FastAPI 就立刻把它通过网络推给客户端。

## 测试流式接口

```sh
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
     -H "Content-Type: application/json" \
     -d '{"session_id": "test_001", "message": "请详细解释一下什么是博格公式，以及如何用它来预估标普500的收益？"}'
```

你会看到控制台里，字符像打字机一样，一块一块地“蹦”出来：

```
data: {"content": "博"}

data: {"content": "格"}

data: {"content": "公式"}

...
```
