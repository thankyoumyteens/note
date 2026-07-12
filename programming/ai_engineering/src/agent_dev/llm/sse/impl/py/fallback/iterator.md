# Iterator 和 yield

`Iterator` 表示迭代器，也就是可以按顺序逐个取出元素的对象。

Python 会通过 `next()` 从迭代器中读取下一个元素。没有更多元素时，迭代器会抛出 `StopIteration` 异常：

```py
numbers = iter([10, 20, 30])  # 根据列表创建迭代器。

print(next(numbers))  # 10
print(next(numbers))  # 20
print(next(numbers))  # 30
try:
    next(numbers)  # 抛出 StopIteration，表示迭代结束。
except StopIteration:
    print("StopIteration")
```

`for` 循环会自动完成这个过程：

```py
for number in iter([10, 20, 30]):
    # 每轮循环调用一次 next()，直到收到 StopIteration。
    print(number)
```

## Iterable 和 Iterator

`Iterable` 表示“可以被遍历的对象”，例如 `list`。`Iterator` 不仅可以被遍历，还会保存当前遍历位置。

```py
numbers = [10, 20, 30]  # list 是 Iterable。
iterator = iter(numbers)  # iter() 根据 Iterable 创建 Iterator。

print(next(iterator))  # 10
print(next(iterator))  # 20，Iterator 记住了上次的位置。
```

## yield

普通函数使用 `return` 一次性返回结果并结束执行。函数中只要出现 `yield`，它就会成为生成器函数。

调用生成器函数时，函数体不会立即完整执行，而是返回一个 `Generator`。`Generator` 是一种 `Iterator`：

```py
from collections.abc import Iterator


def generate_numbers() -> Iterator[int]:
    """逐个生成数字。"""
    print("开始执行")
    yield 10  # 返回 10，并暂停在这里。
    yield 20  # 下次调用 next() 时，从上次暂停处继续。
    yield 30


numbers = generate_numbers()  # 此时函数体还没有开始执行。

print(next(numbers))  # 输出“开始执行”，然后得到 10。
print(next(numbers))  # 得到 20。
print(next(numbers))  # 得到 30。
next(numbers)  # 函数执行完毕，抛出 StopIteration。
```

`yield` 同时完成两个动作：

1. 向调用方返回一个元素。
2. 保存当前函数的局部变量和执行位置，等待下一次 `next()` 后继续执行。

因此，生成器适合处理不能或不应该一次性放入内存的数据，例如文件、分页结果和 LLM 流式响应。

## 项目中的 Iterator

`LlmStreamProviderClient.stream()` 的返回类型是：

```py
def stream(
    self,
    request: UnifiedChatRequest,
) -> Iterator[UnifiedChatStreamEvent]:
    """逐个返回统一流式事件。"""
```

`Iterator[UnifiedChatStreamEvent]` 表示每次调用 `next()`，都会得到一个 `UnifiedChatStreamEvent`。

ProviderClient 收到一个模型 chunk 后，通过 `yield` 返回一个统一事件：

```py
def _stream_once(self, request: UnifiedChatRequest) -> Iterator[UnifiedChatStreamEvent]:
    stream = self.client.chat.completions.create(..., stream=True)

    for chunk in stream:
        content = chunk.choices[0].delta.content

        if content:
            # 返回当前增量内容，然后暂停并等待调用方读取下一个事件。
            yield UnifiedChatStreamEvent(
                type=StreamEventType.MESSAGE,
                provider=self._provider,
                model=chunk.model or self._model,
                content=content,
            )
```

Router 再消费 ProviderClient 的 Iterator，并把事件继续向上返回：

```py
def stream(self, request: UnifiedChatRequest) -> Iterator[UnifiedChatStreamEvent]:
    for client in self.clients:
        content_started = False

        for event in client.stream(request):
            if event.type == StreamEventType.MESSAGE:
                content_started = True

            # 不把所有事件收集成 list，而是收到一个就向上返回一个。
            yield event
```

`sse_main.py` 中的 `event_generator()` 最后把统一事件转换成 SSE 文本：

```py
def event_generator() -> Iterator[str]:
    for event in router.stream(request):
        # FastAPI 每读取一次，就向浏览器发送一个 SSE 事件。
        yield sse_event(event)
```

完整调用链是：

```text
LLM SDK stream
    → ProviderClient Iterator
    → Router Iterator
    → event_generator Iterator
    → StreamingResponse
    → 浏览器
```

浏览器需要下一段数据时，FastAPI 才会继续读取 `event_generator`；每一层再向下一层读取一个元素。这种按需拉取方式不会等待模型生成完成，也不需要把完整回答保存到内存后再返回。

## Iterator 的结束和关闭

生成器自然执行完毕或执行 `return` 时，会向调用方表现为 `StopIteration`：

```py
def generate_once() -> Iterator[str]:
    yield "message"
    return  # 结束生成器，后续 next() 会抛出 StopIteration。
```

调用方也可以主动关闭生成器：

```py
generator = generate_once()
generator.close()  # 在生成器内部触发 GeneratorExit。
```

这与 SSE 客户端断流有关：客户端断开后，响应生成器需要停止执行，并继续关闭 Router、ProviderClient 和 SDK stream，避免模型在前端不再接收时继续生成。
