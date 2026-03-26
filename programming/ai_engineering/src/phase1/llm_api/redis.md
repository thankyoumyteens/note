# 引入真正的 Redis

就像在分布式系统中用 Redis 生成全局唯一流水号来应对高并发一样，在 AI 对话场景里，我们引入 Redis 也是为了解决状态一致性问题：无论 Nginx 把用户的下一次请求打到集群里的哪台机器上，AI 都能根据 Session ID 准确找回它的“记忆”。

在这里，我不仅会带你连上 Redis，还会直接教你生产环境中最核心的两个防坑技巧：

1. 系统预设分离：绝对不能把 System Prompt 存进 Redis，否则后面清理冗余记忆时会把它误删，导致 AI “人设崩塌”。
2. 滑动窗口限流 (Sliding Window)：大模型按 Token 收费且有上下文长度上限。如果不加限制，聊上两百回合，单次请求的费用会极其高昂，甚至直接报错。我们必须利用 Redis 的 LTRIM 指令，只保留最近的 N 轮对话。

### 1. 安装依赖

安装 Python 的 Redis 客户端

```sh
pip install redis
```

### 2. 代码

```py
import os

import env_setup

import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import AsyncOpenAI
import redis.asyncio as redis  # 【关键1】引入异步 Redis 客户端

app = FastAPI()

client = AsyncOpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url="https://api.siliconflow.cn/v1"
)

# 初始化 Redis 客户端
# 生产环境建议将配置写进环境变量，decode_responses=True 会自动将字节解码为字符串
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


class ChatRequest(BaseModel):
    session_id: str
    message: str


# 固定的系统人设，不存入数据库，每次请求时动态拼装
SYSTEM_PROMPT = {
    "role": "system",
    "content": "你是一个在华尔街摸爬滚打多年的顶尖交易员。你极度看重基本面数据（如 ROE、P/E 估值、盈利收益率），说话一针见血、极其毒舌，带着对散户的轻视。你的回答要短平快。"
}

# 设定最多记住最近的几条消息（防止 Token 爆炸，10条代表最近的5个回合）
MAX_HISTORY_LENGTH = 10
# 设置会话过期时间（秒），比如 1 小时没说话，就清空记忆释放内存
SESSION_TTL = 3600


async def generate_chat_stream(session_id: str, user_message: str):
    redis_key = f"chat_history:{session_id}"

    # 1. 从 Redis 读取历史记录 (只包含 user 和 assistant 的对话)
    # LRANGE 获取列表中的所有元素
    raw_history = await redis_client.lrange(redis_key, 0, -1)

    # 将 Redis 里的 JSON 字符串反序列化为 Python 字典列表
    history_messages = [json.loads(msg) for msg in raw_history]

    # 2. 动态拼装本次请求的完整上下文 = 系统人设 + 历史记录 + 当次新问题
    new_user_msg = {"role": "user", "content": user_message}

    request_messages = [SYSTEM_PROMPT] + history_messages + [new_user_msg]

    try:
        # 3. 发起大模型流式请求
        response = await client.chat.completions.create(
            model="Pro/moonshotai/Kimi-K2.5",
            messages=request_messages,
            temperature=0.8,
            stream=True
        )

        full_reply = ""

        async for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_reply += content

                payload = json.dumps({"content": content}, ensure_ascii=False)
                yield f"data: {payload}\n\n"

        # 4. 【异步后置处理】：流式输出完毕后，更新 Redis 记忆
        new_ai_msg = {"role": "assistant", "content": full_reply}

        # 使用管道 (Pipeline) 保证批量操作的原子性和减少网络 I/O 的往返开销
        async with redis_client.pipeline(transaction=True) as pipe:
            # 将新的用户问题和 AI 回答追加到 Redis 列表右侧
            pipe.rpush(redis_key, json.dumps(new_user_msg))
            pipe.rpush(redis_key, json.dumps(new_ai_msg))

            # 【核心护城河】：滑动窗口裁剪。只保留列表最右边（最新）的 MAX_HISTORY_LENGTH 条记录
            pipe.ltrim(redis_key, -MAX_HISTORY_LENGTH, -1)

            # 刷新过期时间
            pipe.expire(redis_key, SESSION_TTL)

            # 把打包在 Pipeline 里的 RPUSH、LTRIM 和 EXPIRE 指令一次性发给 Redis
            await pipe.execute()

        yield "data: [DONE]\n\n"

    except Exception as e:
        error_payload = json.dumps({"error": f"系统异常: {str(e)}"}, ensure_ascii=False)
        yield f"data: {error_payload}\n\n"


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
