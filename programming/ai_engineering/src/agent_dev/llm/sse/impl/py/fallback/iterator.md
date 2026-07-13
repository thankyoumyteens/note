# AsyncIterator 和 yield

`AsyncIterator` 表示异步迭代器。它与普通 `Iterator` 一样逐个返回元素，但获取下一个元素时允许执行异步等待，因此适合读取网络流、数据库游标和 LLM 流式响应。

## anext 和 async for

普通 Iterator 使用 `next()`；AsyncIterator 使用 `await anext()`。没有更多元素时，异步迭代器会抛出 `StopAsyncIteration`：

```py
import asyncio
from collections.abc import AsyncIterator


async def generate_numbers() -> AsyncIterator[int]:
    """异步逐个生成数字。"""
    for number in [10, 20, 30]:
        await asyncio.sleep(0.1)  # 模拟异步等待数据。
        yield number


async def main() -> None:
    numbers = generate_numbers()  # 创建异步生成器。

    print(await anext(numbers))  # 10
    print(await anext(numbers))  # 20
    print(await anext(numbers))  # 30

    try:
        await anext(numbers)  # 没有更多元素时抛出 StopAsyncIteration。
    except StopAsyncIteration:
        print("StopAsyncIteration")


asyncio.run(main())
```

实际代码通常使用 `async for` 自动读取，直到收到 `StopAsyncIteration`：

```py
import asyncio
from collections.abc import AsyncIterator


async def generate_numbers() -> AsyncIterator[int]:
    """异步逐个生成数字。"""
    for number in [10, 20, 30]:
        await asyncio.sleep(0.1)  # 模拟异步等待数据。
        yield number


async def main() -> None:
    async for number in generate_numbers():
        # 每轮循环异步等待一个元素，不会阻塞事件循环。
        print(number)


asyncio.run(main())
```

## async yield

Python 没有单独的 `async yield` 关键字。只要在 `async def` 中使用 `yield`，这个函数就会成为异步生成器函数：

```py
from collections.abc import AsyncIterator


async def generate_messages() -> AsyncIterator[str]:
    yield "第一段"  # 返回一个元素，并暂停当前异步生成器。
    yield "第二段"  # 下次 anext() 时从这里继续。
```

调用异步生成器函数时，函数体不会立即完整执行，而是返回一个异步生成器。每次 `await anext()` 或进入下一轮 `async for` 时，函数才继续运行到下一个 `yield`。

`yield` 会：

1. 向调用方返回当前元素。
2. 保存局部变量和执行位置。
3. 暂停生成器，等待调用方异步请求下一个元素。

## Iterator 和 AsyncIterator 的区别

```text
Iterator
    next(iterator)
    for item in iterator
    阻塞等待下一个元素

AsyncIterator
    await anext(iterator)
    async for item in iterator
    等待期间释放事件循环
```

LLM chunk 来自网络。如果使用同步 Iterator，SDK 等待下一个 chunk 时会阻塞当前线程；使用 AsyncIterator 时，事件循环可以继续处理其他请求和客户端断开事件。

## 项目中的 AsyncIterator

`LlmStreamProviderClient.stream()` 返回：

```py
def stream(
    self,
    request: UnifiedChatRequest,
) -> AsyncIterator[UnifiedChatStreamEvent]:
    """返回统一异步流式事件。"""
```

具体 ProviderClient 使用异步生成器实现：

```py
async def _stream_once(
    self,
    request: UnifiedChatRequest,
) -> AsyncIterator[UnifiedChatStreamEvent]:
    stream = await self.client.chat.completions.create(
        model=self._model,
        messages=[],
        stream=True,
    )

    async with stream:
        async for chunk in stream:
            content = chunk.choices[0].delta.content

            if content:
                # 收到一个模型 chunk，就向上返回一个统一事件。
                yield UnifiedChatStreamEvent(
                    type=StreamEventType.MESSAGE,
                    provider=self._provider,
                    model=chunk.model or self._model,
                    content=content,
                )
```

Router 使用 `async for` 消费 ProviderClient，再继续向上 `yield`：

```py
async def stream(
    self,
    request: UnifiedChatRequest,
) -> AsyncIterator[UnifiedChatStreamEvent]:
    for client in self.clients:
        async for event in client.stream(request):
            # 不收集成 list，收到一个事件就向上返回一个事件。
            yield event
```

FastAPI 的响应生成器继续消费 Router：

```py
async def event_generator() -> AsyncIterator[str]:
    async for event in router.stream(request):
        # StreamingResponse 收到一个字符串就向浏览器发送一个 SSE 事件。
        yield sse_event(event)
```

完整调用链是：

```text
异步 LLM SDK stream
    → ProviderClient AsyncIterator
    → Router AsyncIterator
    → event_generator AsyncIterator
    → StreamingResponse
    → 浏览器
```

## 结束、关闭与取消

异步生成器自然执行完毕或执行 `return` 时，会向调用方表现为 `StopAsyncIteration`：

```py
from collections.abc import AsyncIterator


async def generate_once() -> AsyncIterator[str]:
    yield "message"
    return  # 后续 anext() 会抛出 StopAsyncIteration。
```

调用方可以使用 `await generator.aclose()` 主动关闭异步生成器：

```py
async def close_generator() -> None:
    generator = generate_once()
    await generator.aclose()  # 主动关闭异步生成器。
```

FastAPI 客户端断开时，当前异步响应任务会被取消。正在等待模型 chunk 的异步生成器会收到 `asyncio.CancelledError`，因此 Controller 必须继续抛出取消异常，并让各层的 `async with` 或 `aclosing` 关闭上游资源：

```py
import asyncio
from collections.abc import AsyncIterator


async def event_generator() -> AsyncIterator[str]:
    try:
        async for event in router.stream(request):
            yield sse_event(event)
    except asyncio.CancelledError:
        # 不吞掉取消信号，让上游异步生成器继续执行关闭逻辑。
        raise
```

与同步 Iterator 依赖线程池不同，这条异步调用链可以直接接收 ASGI 任务取消信号，更适合 FastAPI SSE。

## 与 Java 实现的区别

`AsyncIterator` 和异步生成器是 Python 语法，Spring Boot + WebClient 和 Spring AI 不使用这套写法，因此这里不再提供两套 Java 实现。

Java 项目中的 Reactor `Flux` 同样支持逐个传递元素和取消传播，但它属于响应式流，不等同于 Python 的 AsyncIterator。

## 运行示例

这些基础示例只使用 Python 标准库：

```sh
uv run python main.py
```
