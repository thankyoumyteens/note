# 封装成一个支持异步流式输出的 Web API

把大模型的流式输出对接到前端，最标准的协议不是 WebSocket，而是 SSE (Server-Sent Events)。

WebSocket 是双向通讯，用来做实时多人游戏很合适，但大模型聊天是典型的“单向流”：你发一个完整的 HTTP 请求过去，服务器像挤牙膏一样源源不断地把文本推回来。SSE 完美契合这个场景，而且比 WebSocket 轻量得多。

为了扛住高并发，我们要发挥 Python 的异步优势。在 Java 传统 Web 框架中，一个请求往往会霸占一个线程，如果遇到大模型接口响应慢，线程池很容易被打满导致整个应用阻塞。而在 FastAPI 中，借助 ASGI（异步服务器网关接口）和事件循环，我们在等待大模型返回数据时让出 CPU，用极少的线程就能处理海量并发。

安装一下 FastAPI 和对应的 ASGI 服务器:

```sh
pip install fastapi uvicorn
```

FastAPI + SSE 异步流式接口:

```py
import os
import json
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import AsyncOpenAI  # 【关键1】必须使用异步版本的 OpenAI 客户端

app = FastAPI()

# 初始化异步客户端
client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)


# 定义前端传过来的请求体
class ChatRequest(BaseModel):
    session_id: str  # 用来区分不同用户的会话
    message: str  # 用户的提问


# 【模拟外部缓存】：在真实的分布式系统中，千万不要用全局变量存状态！
# 你需要用 Redis 结合 session_id 来存取历史记录，甚至可以利用 Redis 生成唯一的自增 ID 作为消息流水号。
fake_redis_cache = {}


async def generate_chat_stream(session_id: str, user_message: str):
    """
    这是一个异步生成器 (Async Generator)，通过 yield 关键字不断向前端吐出数据
    """
    # 1. 从缓存加载对话上下文
    if session_id not in fake_redis_cache:
        fake_redis_cache[session_id] = [
            {"role": "system",
             "content": "你是一个在华尔街摸爬滚打多年的顶尖交易员。你极度看重基本面数据，说话一针见血、极其毒舌。"}
        ]

    messages = fake_redis_cache[session_id]
    messages.append({"role": "user", "content": user_message})

    try:
        # 2. 调用大模型 (注意这里是 await，不会阻塞主线程)
        response = await client.chat.completions.create(
            model="ep-11111111111111-aaaaa",
            messages=messages,
            temperature=0.8,
            stream=True
        )

        full_reply = ""

        # 3. 异步迭代流式响应
        async for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_reply += content

                # 为了前端好解析，我们把文本包在一个 JSON 对象里
                payload = json.dumps({"content": content}, ensure_ascii=False)
                # 【关键】SSE 格式规范：必须以 "data: " 开头，以 "\n\n" 结尾
                yield f"data: {payload}\n\n"

        # 4. 只有在流式输出完全结束后，才把完整的一句话存入缓存
        messages.append({"role": "assistant", "content": full_reply})
        fake_redis_cache[session_id] = messages

        # 5. 发送结束标志，通知前端可以关闭连接了
        yield "data: [DONE]\n\n"

    except Exception as e:
        # 异常处理：通知前端报错，并把刚才加进去的用户问题弹出来，保证上下文干净
        error_payload = json.dumps({"error": f"华尔街连线中断: {str(e)}"}, ensure_ascii=False)
        yield f"data: {error_payload}\n\n"
        messages.pop()


@app.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    # 【关键】使用 FastAPI 的 StreamingResponse，并指定 media_type 为 text/event-stream
    return StreamingResponse(
        generate_chat_stream(request.session_id, request.message),
        media_type="text/event-stream"
    )


if __name__ == "__main__":
    import uvicorn

    # 启动服务，运行在 8000 端口
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

因为这是流式接口，用普通的浏览器地址栏或者 Postman 不太好直观测试。你可以直接打开终端，用 curl 模拟前端请求。注意看终端里数据是怎么一段一段打印出来的：

```sh
# macOS/Linux 测试命令
curl -X POST "http://127.0.0.1:8000/chat/stream" \
     -H "Content-Type: application/json" \
     -d '{"session_id": "user_001", "message": "我想定投沪深300，你觉得现在的估值怎么样？"}'
```

你会看到类似这样的输出，就像水管里的水一样流出来：

```
data: {"content": "定"}

data: {"content": "投"}

data: {"content": "沪"}

data: {"content": "深"}

...
data: [DONE]
```

## 核心点

1. AsyncOpenAI 与 await：这是解决 I/O 密集型任务（等待大模型服务器响应）的利器。当 await 触发时，当前请求挂起，底层框架会立刻去处理其他用户的并发请求，彻底告别了传统多线程模型中的线程饿死和上下文切换开销。
2. yield 生成器：Python 的 yield 让函数变成了一个可以暂停和恢复的状态机。每次大模型返回一个 Token 的碎片，我们就 yield 一下，FastAPI 就会立刻把这个碎片通过 HTTP 长连接推给客户端。
3. SSE 格式协议：`data: {...}\n\n`。前端只需要使用原生的 EventSource API 或者 fetch API 就能轻松解析这个流，并实时更新到 UI 上，实现大家最熟悉的 ChatGPT 打字机效果。
