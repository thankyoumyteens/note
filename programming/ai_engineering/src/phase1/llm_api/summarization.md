# 增加摘要记忆

滑动窗口虽然能控制成本，但最大的痛点是**“彻底的遗忘”**。如果用户在第一轮对话里说“我手里有 100 万闲钱，风险承受能力很低”，聊到第 20 轮的时候，滑动窗口早就把这句话删了，那个毒舌交易员可能就会直接推荐高风险的期权，这就酿成了严重的业务事故。

为了解决这个问题，业界最成熟的架构是：短期记忆（滑动窗口） + 长期记忆（滚动摘要 Rolling Summary）。

在 Java 里，如果你遇到一个耗时很长的任务（比如调用大模型做摘要），你通常会把它扔进线程池，让它在后台慢慢跑，不要阻塞当前给用户的响应。在 FastAPI 里，我们有原生的等价物：BackgroundTasks。

架构设计思路

1. 短记忆 (Short-Term)：依然用 Redis List `chat_history:{session_id}`，但容量可以设小一点，比如只存最近 6 条（3 个回合）。
2. 长记忆 (Long-Term)：新增一个 Redis String `chat_summary:{session_id}`，专门存过去对话的浓缩摘要。

每次组装请求发给大模型时，我们的结构变成了：

```
System Prompt + [后台摘要] + [最近的 6 条聊天记录] + [当前新问题]。
```

修改 main.py。这次引入了 BackgroundTasks 来做异步的摘要压缩：

```py
import json
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import AsyncOpenAI
import redis.asyncio as redis
import asyncio  # 【新增】引入 Python 内置的异步库
from fastapi import FastAPI, BackgroundTasks  # 【新增】引入后台任务

app = FastAPI()

client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)


class ChatRequest(BaseModel):
    session_id: str
    message: str


SYSTEM_PROMPT = {
    "role": "system",
    "content": "你是一个在华尔街摸爬滚打多年的顶尖交易员。你极度看重基本面数据（如 ROE、P/E 估值、盈利收益率），说话一针见血、极其毒舌，带着对散户的轻视。你的回答要短平快。"
}

# 触发摘要的阈值（当历史记录达到 8 条，也就是 4 个回合时触发）
SUMMARY_THRESHOLD = 8

SESSION_TTL = 3600


# ==========================================
# 【核心逻辑】：后台异步执行的摘要压缩任务
# ==========================================
async def compress_memory_task(session_id: str):
    history_key = f"chat_history:{session_id}"
    summary_key = f"chat_summary:{session_id}"

    # 1. 拿到当前的旧摘要和过长的历史记录
    old_summary = await redis_client.get(summary_key) or "无"
    raw_history = await redis_client.lrange(history_key, 0, -1)

    if len(raw_history) < SUMMARY_THRESHOLD:
        return  # 如果不够长，说明被其他并发请求处理过了，直接退出

    history_text = "\n".join([json.loads(msg)["content"] for msg in raw_history])

    # 2. 召唤大模型，让它自己总结自己
    # 注意：这里我们单独开一个全新的对话上下文
    summarize_prompt = f"""
    请作为旁观者，总结以下对话历史。
    之前的摘要：{old_summary}
    新增的对话：{history_text}
    要求：将核心事实、用户的偏好（如关注的指标、资金量等）提取出来，生成一段不超过 150 字的精简摘要。不要保留寒暄废话。
    """

    try:
        # 这里不需要流式输出，直接一次性等待结果即可
        response = await client.chat.completions.create(
            # 摘要任务用更便宜的模型即可，降低成本
            model="ep-11111111111111-bbbbb",
            messages=[{"role": "user", "content": summarize_prompt}],
            temperature=0.3  # 摘要需要严谨，降低随机性
            # 不开启流式输出，直接等待结果全部返回
        )

        new_summary = response.choices[0].message.content

        # 3. 将新摘要存入 Redis，并清空刚刚被总结过的那部分历史记录
        # 我们留下最新的 2 条（1 个回合），保持对话的连贯性
        async with redis_client.pipeline(transaction=True) as pipe:
            pipe.setex(summary_key, SESSION_TTL, new_summary)
            pipe.ltrim(history_key, -2, -1)
            await pipe.execute()

        print(f"[{session_id}] 摘要压缩完成：{new_summary}")

    except Exception as e:
        print(f"摘要压缩失败: {e}")


# ==========================================
# 主流式接口
# ==========================================
async def generate_chat_stream(session_id: str, user_message: str, background_tasks: BackgroundTasks):
    history_key = f"chat_history:{session_id}"
    summary_key = f"chat_summary:{session_id}"

    # 1. 并发获取历史记录和当前的摘要
    raw_history, current_summary = await asyncio.gather(
        redis_client.lrange(history_key, 0, -1),
        redis_client.get(summary_key)
    )

    history_messages = [json.loads(msg) for msg in raw_history]

    # 2. 组装终极 Context
    request_messages = [SYSTEM_PROMPT]

    if current_summary:
        # 如果有摘要，把它变成一条 System 指令塞进去，大模型会把它当成“已知事实”
        request_messages.append({"role": "system", "content": f"【用户历史背景摘要】：{current_summary}"})

    request_messages.extend(history_messages)
    new_user_msg = {"role": "user", "content": user_message}
    request_messages.append(new_user_msg)

    try:
        response = await client.chat.completions.create(
            # 这里使用更强的模型
            model="ep-11111111111111-aaaaa",
            messages=request_messages,
            temperature=0.8,
            stream=True
        )

        full_reply = ""
        async for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_reply += content
                yield f"data: {json.dumps({'content': content}, ensure_ascii=False)}\n\n"

        new_ai_msg = {"role": "assistant", "content": full_reply}

        # 保存对话记录
        async with redis_client.pipeline(transaction=True) as pipe:
            pipe.rpush(history_key, json.dumps(new_user_msg))  # type: ignore
            pipe.rpush(history_key, json.dumps(new_ai_msg))  # type: ignore
            pipe.expire(history_key, SESSION_TTL)  # type: ignore
            await pipe.execute()

        # 3. 【核心触发机制】：如果对话太长了，触发后台压缩任务
        # 我们不需要在这里 await 等它做完，直接交给 FastAPI 的事件循环在后台慢慢跑
        if len(history_messages) + 2 >= SUMMARY_THRESHOLD:
            background_tasks.add_task(compress_memory_task, session_id)

        yield "data: [DONE]\n\n"

    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"


# 接口入参加上 BackgroundTasks
@app.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest, background_tasks: BackgroundTasks):
    return StreamingResponse(
        generate_chat_stream(request.session_id, request.message, background_tasks),
        media_type="text/event-stream"
    )


if __name__ == "__main__":
    import uvicorn

    # 启动服务，运行在 8000 端口
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 为什么这套架构是极其优雅的？

1. 绝对不阻塞用户：在 Java 里你可能需要配置线程池和 CompletableFuture。在这里，`background_tasks.add_task` 直接把压缩任务扔到了事件循环里。用户在前端看到“毒舌交易员”刚刚喷完最后半句话，后台其实已经悄悄开始启动另一个大模型（便宜的 GPT-3.5）去压缩记忆了。用户的下一个请求发过来时，感受不到任何卡顿。
2. 成本与智商的最佳平衡：
   - 陪用户聊天、解答 P/E 估值这种高难度推演，我们用昂贵的、聪明的模型，比如 GPT-4o。
   - 在后台做文本摘要这种不需要太多逻辑思考的粗活，我们用极其便宜的模型，比如 GPT-3.5-turbo。
   - 这是企业级 AI 开发最常用的“大小模型协同”降本增效策略。
3. 记忆永不断档：即使用户聊了几个小时，哪怕是最早告诉 AI 的资金体量和风险偏好，也会被安全地浓缩在 chat_summary 里，作为系统设定的强制前置条件，时刻约束着大模型的行为。
