# 异步编程

在 AI 应用开发中，这一块的优先级是最高的。为什么？因为调用大模型 API（比如 OpenAI、Claude 或国内的各种大模型）是一个极其耗时的 I/O 密集型操作。一个请求等上 3~10 秒是家常便饭，如果用传统的同步代码，你的服务分分钟就会被几个并发请求卡死。

对于 Java 开发者来说，理解 Python 的异步需要一次小小的“思维转换”。

多线程 vs 事件循环：

- ☕️ Java 传统并发（JDK 21 虚拟线程前）： 遇到耗时任务，通常是扔进线程池（Thread Pool）或者用 `CompletableFuture`。核心逻辑是 **“多雇几个服务员（线程）”**，每个服务员专职服务一桌客人，阻塞了就干等。
- 🐍 Python 异步 (asyncio)： Python 受制于全局解释器锁（GIL），多线程效率并不高。因此它采用了类似 Node.js 的 **“单线程事件循环（Event Loop）”。核心逻辑是“一个超级服务员”**，给这桌点完菜（发请求），不留在原地等厨师做菜，而是立刻去服务下一桌。菜做好了（I/O 返回），再回来端菜（执行后续逻辑）。

## 核心语法：async 与 await

在 Python 中，异步编程的标志就是这两个关键字。

- `async def`：把一个普通函数变成一个“协程”（Coroutine）。调用它不会立刻执行，而是返回一个协程对象。
- `await`：交出控制权。告诉事件循环：“我在这里卡住了（等网络、等读写），你去忙别人的事吧，有了结果再叫醒我。”

```py
import asyncio
import time

# 传统的同步函数 (阻塞型)
def sync_call():
    print("同步：开始请求...")
    time.sleep(2)  # 线程在这里彻底死等 2 秒
    print("同步：请求完成！")

# 异步的协程函数 (非阻塞型)
async def async_call():
    print("异步：开始请求...")
    # 遇到 await，把线程的控制权交还给事件循环，去跑别的任务
    await asyncio.sleep(2)
    print("异步：请求完成！")
```

## AI 实战场景：并发请求大模型

假设你需要同时向大模型发送 3 个问题，如果串行（排队）请求，每个耗时 2 秒，总共需要 6 秒。但在异步模式下，总耗时接近 2 秒。

```py
import asyncio

async def call_llm(prompt: str):
    print(f"[{prompt}] 正在发送请求...")
    await asyncio.sleep(2) # 模拟大模型思考了 2 秒
    return f"[{prompt}] 的回答"

async def main():
    print("开始并发测试...")

    # asyncio.gather 类似 Java 的 CompletableFuture.allOf()
    # 它会并发执行所有传入的协程，并按照传入顺序返回一个结果列表
    results = await asyncio.gather(
        call_llm("写个文案"),
        call_llm("翻译句子"),
        call_llm("写段代码")
    )

    print("全部完成，结果：", results)

# Python 程序的异步入口，用来启动事件循环
if __name__ == "__main__":
    asyncio.run(main())
```

## Java 开发者最容易踩的“致命天坑”

在 Python 的异步函数里，绝对不能写同步阻塞的代码！

因为 Python 只有一个“超级服务员（单线程）”。如果你在一个 `async def` 函数里写了 `time.sleep(10)` 或者用老式的同步库发起网络请求，这个唯一的服务员就会被彻底卡住，导致整个服务假死，其他并发请求全部超时。

- 错误示范 ❌： 在异步里用 `requests` 库（它是同步的）。
- 正确示范 ✅： 改用支持异步的 HTTP 库，比如 `httpx` 或 `aiohttp`。

正确的 AI 异步网络请求：

```py
import asyncio
# pip install httpx
import httpx

async def fetch_api(url: str):
    # 使用 httpx.AsyncClient() 替代 requests
    async with httpx.AsyncClient() as client:
        # 必须加 await！
        response = await client.get(url)
        return response.json()
```
