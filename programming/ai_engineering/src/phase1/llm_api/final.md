# Function Calling 融入 SSE 流式输出

在流式输出（Streaming）开启的情况下，处理 Function Calling 是极其复杂的。因为当大模型决定调用工具时，它返回的不再是一个完整的 JSON 指令，而是一块一块的 JSON 碎片（Chunks）。

这就要求我们在后端做一件事：拦截并拼接碎片，执行工具，发起二次请求。

整个流程变成了：

1. 一轮流式请求：监听流。如果大模型输出普通文本，直接推给前端；如果它开始吐出工具参数的碎片，我们在内存里悄悄把它们拼起来。
2. 中途拦截：发现拼完了一个完整的工具调用指令，暂停向前端输出，本地执行 Python 函数查数据。
3. 二轮流式请求：把查到的数据塞回去，再次调用大模型，把大模型最终润色后的毒舌回答流式推给前端。

```py
import os

import env_setup

import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import AsyncOpenAI
import redis.asyncio as redis
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境下允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = AsyncOpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.siliconflow.cn/v1"
)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


class ChatRequest(BaseModel):
    session_id: str
    message: str


SYSTEM_PROMPT = {
    "role": "system",
    "content": "你是一个在华尔街摸爬滚打多年的顶尖交易员。极其毒舌，极度看重基本面。你会使用工具获取真实数据来狠狠地教育散户。"
}


# ==========================================
# 1. 你的本地“武器库”
# ==========================================
def get_index_valuation(index_name: str) -> str:
    """本地查库逻辑"""
    if "人工智能" in index_name or "AI" in index_name.upper():
        # 返回精确的行情数据
        return json.dumps({
            "index_name": "中证人工智能主题指数",
            "current_point": 5566.15,
            "pe_ratio": 45.2,
            "status": "极度高估，泡沫严重"
        }, ensure_ascii=False)
    return json.dumps({"error": "未找到该指数数据"})


TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_index_valuation",
        "description": "获取指定股票指数的最新点位和市盈率估值数据。",
        "parameters": {
            "type": "object",
            "properties": {"index_name": {"type": "string"}},
            "required": ["index_name"]
        }
    }
}]


# ==========================================
# 2. 核心流式 Agent 逻辑
# ==========================================
async def generate_chat_stream(session_id: str, user_message: str):
    # 从缓存加载对话上下文
    history_key = f"chat_history:{session_id}"
    raw_history = await redis_client.lrange(history_key, 0, -1)
    history_messages = [json.loads(msg) for msg in raw_history]

    new_user_msg = {"role": "user", "content": user_message}
    request_messages = [SYSTEM_PROMPT] + history_messages + [new_user_msg]

    try:
        # 【第一轮请求】：开启流式，带上工具箱
        response = await client.chat.completions.create(
            model="Pro/moonshotai/Kimi-K2.5",
            messages=request_messages,
            tools=TOOLS,
            stream=True
        )

        full_reply = ""
        tool_calls_accumulator = {}  # 用来收集流式的函数调用碎片

        async for chunk in response:
            delta = chunk.choices[0].delta

            # 情况 A：如果大模型正常说话，直接把文字推给前端
            if delta.content is not None:
                content = delta.content
                full_reply += content
                yield f"data: {json.dumps({'content': content}, ensure_ascii=False)}\n\n"

            # 情况 B：【高能预警】如果大模型决定调用工具，它会发来 tool_calls 碎片
            if delta.tool_calls:
                for tc in delta.tool_calls:
                    idx = tc.index  # 碎片的索引
                    if idx not in tool_calls_accumulator:
                        # 初始化这个工具的坑位
                        tool_calls_accumulator[idx] = {
                            "id": tc.id,
                            "type": "function",
                            "function": {"name": tc.function.name, "arguments": ""}
                        }
                    # 不断把 JSON 参数的字符串碎片拼起来
                    if tc.function.arguments:
                        tool_calls_accumulator[idx]["function"]["arguments"] += tc.function.arguments

        # 【拦截判定】：流式结束后，检查刚才有没有积攒工具调用？
        if tool_calls_accumulator:
            # 1. 给前端发一个友好的提示（这步极其提升用户体验！）
            loading_message = json.dumps(
                {'content': '<br><i style=\"color:gray;\">[系统日志：正在切入交易内网查询底层数据...]</i><br>'},
                ensure_ascii=False
            )
            yield f"data: {loading_message}\n\n"

            # 2. 把大模型想要调用的工具列表，存入上下文
            tool_calls_list = list(tool_calls_accumulator.values())
            request_messages.append({"role": "assistant", "tool_calls": tool_calls_list})

            # 3. 循环执行所有被调用的工具
            for tc in tool_calls_list:
                func_name = tc["function"]["name"]
                args_str = tc["function"]["arguments"]
                args = json.loads(args_str)  # 拼凑完毕，终于可以反序列化了

                print(f"[{session_id}] 触发本地调用: {func_name}, 参数: {args}")

                if func_name == "get_index_valuation":
                    # 执行刚才写的本地函数
                    result = get_index_valuation(args.get("index_name", ""))

                    # 把本地查到的结果塞回上下文
                    request_messages.append({
                        "tool_call_id": tc["id"],
                        "role": "tool",
                        "name": func_name,
                        "content": result
                    })

            # 4. 【第二轮请求】：带着查到的真实数据，再次唤醒大模型，让它润色
            second_response = await client.chat.completions.create(
                model="Pro/moonshotai/Kimi-K2.5",
                messages=request_messages,
                stream=True  # 第二次也要流式输出
            )

            async for chunk in second_response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_reply += content
                    yield f"data: {json.dumps({'content': content}, ensure_ascii=False)}\n\n"

        # 最终：把用户的问题，和大模型最终的一大串回复，存入 Redis（调用工具的对话记录不用存）
        new_ai_msg = {"role": "assistant", "content": full_reply}
        async with redis_client.pipeline(transaction=True) as pipe:
            pipe.rpush(history_key, json.dumps(new_user_msg))
            pipe.rpush(history_key, json.dumps(new_ai_msg))
            pipe.ltrim(history_key, -10, -1)
            pipe.expire(history_key, 3600)
            await pipe.execute()

        yield "data: [DONE]\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'error': f'系统崩溃: {str(e)}'}, ensure_ascii=False)}\n\n"


@app.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    return StreamingResponse(
        generate_chat_stream(request.session_id, request.message),
        media_type="text/event-stream"
    )


if __name__ == "__main__":
    import uvicorn

    # 启动服务，运行在 8000 端口
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

1. 在前端输入框里问他：“帮我看看中证人工智能主题指数现在能买吗？”
2. 你会看到极具科幻感的画面：
   1. 它一开始可能一言不发。
   2. 突然，屏幕上打印出灰色的斜体字：`[系统日志：正在切入交易内网查询底层数据...]`
   3. 紧接着，大模型拿到了你返回的 5566.15 点位数据，开始像机关枪一样疯狂打字输出极其专业的金融毒舌点评。

这套代码，就是目前市面上最主流的 AI Agent 底层运行机制：

- 面对日常寒暄，它走 情况 A，极速响应。
- 面对需要数据支撑的硬核问题，它走 情况 B，完美处理极其复杂的“异步流式工具调用片段重组”，并与你的本地系统（或者微服务）无缝桥接。
