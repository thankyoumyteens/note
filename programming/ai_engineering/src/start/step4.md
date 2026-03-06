# 流式输出

大模型生成答案是一个字一个字往外蹦的（自回归生成）。如果等几百个字全部生成完再返回，用户的体验会极差。

流式输出，底层协议就是 SSE (Server-Sent Events)。它是一种基于 HTTP 的单向长连接技术。

在 Python 中，实现这个效果异常简单，核心就两个字：yield (生成器) 和 async/await (异步协程)。

### 1. 在 main.py 顶部新增一个 FastAPI 的流式响应组件导入

```py
# 在文件顶部的 import 区域加入这行
from fastapi.responses import StreamingResponse
```

### 2. 替换掉原来的 @app.post("/api/chat") 整个方法

```py
# 注意：去掉原来的 response_model=QueryResponse，因为我们要返回的是数据流，而不是固定的 JSON
@app.post("/api/chat/stream")
async def chat_stream_endpoint(request: QueryRequest):

    # 定义一个异步生成器函数 (相当于 Java 里的 Flux.create 或 SseEmitter.send)
    async def generate_stream():
        try:
            # 核心改变：从 invoke() 变成了 astream() (异步流式调用)
            async for chunk in conversational_rag_chain.astream(
                {"input": request.query},
                config={"configurable": {"session_id": request.session_id}}
            ):
                # LangChain 的 RetrievalChain 会把不同阶段的数据分块吐出
                # 我们只需要提取最终大模型生成的回答 (对应 "answer" 字段)
                if "answer" in chunk:
                    # yield 是 Python 生成器的灵魂，它会像水龙头一样，把这一个字立刻推给前端
                    yield chunk["answer"]

        except Exception as e:
            # 流式传输中的异常处理
            yield f"\n[服务发生异常: {str(e)}]"

    # 使用 FastAPI 的 StreamingResponse 包装生成器，并指定媒体类型为事件流
    return StreamingResponse(generate_stream(), media_type="text/event-stream")
```

### 3. 测试

复制并在终端运行以下命令（注意 -N 参数非常关键，它告诉 curl 不要缓冲，立刻输出收到的数据）：

```sh
curl -N -X POST "http://127.0.0.1:8000/api/chat/stream" \
     -H "Content-Type: application/json" \
     -d '{
           "session_id": "stream-test-01",
           "query": "请详细分析一下 Palantir 这家公司，以及它的估值方法。"
         }'
```
