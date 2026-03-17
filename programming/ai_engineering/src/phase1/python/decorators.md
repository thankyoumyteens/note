# 装饰器

对于 Java 开发者来说，理解 Python 装饰器有一个经典的“思维陷阱”：不要把它等同于 Java 的注解（Annotation）！

Java AOP vs Python 装饰器：

- ☕️ Java 注解 (`@Override`, `@Transactional`)： 它本身只是静态的元数据（Metadata）。如果你只写一个注解，什么都不会发生。必须有一个外部框架（比如 Spring AOP、反射机制）在启动时去扫描它，然后通过动态代理（CGLIB/JDK Proxy）来增强方法。
- 🐍 Python 装饰器 (`@timer`, `@app.get`)： 它本身就是一段可执行的代码（高阶函数）。Python 在加载代码时，会直接把原函数当作参数塞进装饰器里，并把原函数替换成装饰器返回的“包装函数”。

简单来说：Java 靠框架做动态代理，Python 靠语言原生支持“函数包函数”。

## 手写你的第一个装饰器

写装饰器的标准公式是 **“三层套娃”**（虽然通常只写两层，带参数的装饰器写三层）。我们来写一个最常用的：接口耗时统计。

```py
import time

# 第 1 层：接收你要增强的函数 (func) 作为参数
def timer(func):

    # 第 2 层：这就是用来替代原函数的“包装器”
    # *args 和 **kwargs 类似 Java 的 Object... args，用来接收任意数量和类型的参数
    def wrapper(*args, **kwargs):
        start_time = time.time()          # 🔴 前置操作 (类似 @Before)

        result = func(*args, **kwargs)    # 🟢 执行原函数

        end_time = time.time()            # 🔵 后置操作 (类似 @After)
        print(f"[{func.__name__}] 执行耗时: {end_time - start_time:.4f} 秒")

        return result                     # 🟡 返回原函数的结果

    # 必须把包装器函数返回出去，替换掉原函数！
    return wrapper

# === 如何使用 ===
@timer
def call_llm_api(prompt: str):
    print(f"正在发送提示词: {prompt}")
    time.sleep(1.5) # 模拟网络延迟
    return "这是大模型的回答"

# 当你调用 call_llm_api 时，实际运行的是 wrapper 函数
response = call_llm_api("讲个笑话")
```

## AI 工程实战场景：重试机制 @retry

在调用大模型 API 时，网络抖动或并发限流导致报错是常态。在 Java 里你可能会引入 Resilience4j 或 Spring Retry，而在 Python 里，几十行代码手写一个 `@retry` 装饰器就搞定了。

```py
import time

# 外层：接收装饰器自身的配置参数
def retry(max_retries=3, delay=2):
    # 中层：接收目标函数
    def decorator(func):
        # 内层：包装执行逻辑
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs) # 尝试执行
                except Exception as e:
                    print(f"第 {attempt + 1} 次请求失败: {e}")
                    if attempt < max_retries - 1:
                        print(f"等待 {delay} 秒后重试...")
                        time.sleep(delay)
                    else:
                        print("达到最大重试次数，放弃！")
                        raise e # 抛出最终异常
        return wrapper
    return decorator

# 使用场景：最多重试 3 次，每次间隔 2 秒
@retry(max_retries=3, delay=2)
def unstable_api_call():
    # 模拟偶发的网络异常
    raise ConnectionError("Connection Timeout!")

unstable_api_call() # 运行会看到重试过程
```

## 保护元数据

在上面的例子中，如果你去打印 `call_llm_api.__name__`（获取函数名），你会发现它变成了 "`wrapper`"！因为原函数已经被替换掉了。在复杂的工程中，这会导致 Debug 困难，或者让一些依赖函数签名的框架（如 FastAPI）报错。

解决方案：使用 Python 内置的 `@wraps`。它是专门用来“装饰包装器”的装饰器，作用是把原函数的名字、注释等元数据拷贝过来。

```py
from functools import wraps

def timer(func):
    @wraps(func)  # 加上这一行，找回 Java 反射时的安全感！
    def wrapper(*args, **kwargs):
        # ... 逻辑同上 ...
        return func(*args, **kwargs)
    return wrapper
```

## `*args` 和 `**kwargs`

其实，args 和 kwargs 只是程序员们约定俗成的变量名（你叫 `*a` 和 `**b` 完全可以，但可能会被同事打）。真正的魔法在于 `*`（一颗星）和 `**`（两颗星）。

### `*args`：位置参数的“打包箱” (类似 Java 的可变参数)

在 Java 中，如果你不确定要传几个参数，你会用 `...`。Python 里对应的就是 `*`。它会把所有传入的 **「没有名字的参数（位置参数）」**，打包成一个元组（Tuple，你可以理解为不可变的 List）。

Java 的可变参数:

```java
public void printAll(String... args) {
    for (String arg : args) {
        System.out.println(arg);
    }
}
// 调用
printAll("apple", "banana", "cherry");
```

Python 的 `*args`:

```py
def print_all(*args):
    # 此时 args 是一个元组: ('apple', 'banana', 'cherry')
    print(type(args))
    for arg in args:
        print(arg)

# 调用时，随便传几个位置参数都可以
print_all("apple", "banana", "cherry")
```

### `**kwargs`：关键字参数的“打包箱” (Java 痛点解决者)

Java 原生不支持“命名参数”，如果你想传一堆不确定的键值对，通常只能传一个 `Map<String, Object>` 或者构造一个复杂的 `Builder`。

Python 用 `**` 优雅地解决了这个问题。它会把所有传入的 **「有名字的参数（关键字参数 / Keyword Arguments）」**，打包成一个字典（Dict）。

```py
def print_info(**kwargs):
    # 此时 kwargs 已经被打包成了一个字典: {'name': 'Alice', 'age': 25}
    print(type(kwargs))

    for key, value in kwargs.items():
        print(f"{key}: {value}")

# 调用时，直接写 键=值
print_info(name="Alice", age=25, role="Admin")
```

在写装饰器或者做 API 路由转发时，你的“包装函数”往往不知道“原函数”到底需要什么参数。把 `*args` 和 `**kwargs` 放在一起，就等于声明了：“不管你传什么神仙参数，我全盘接收！”

### 打包 (Packing) vs 解包 (Unpacking)

- 在函数定义处 `def func(*args, **kwargs)`: -> 星号的作用是 **「打包」**。把散落的参数装进 Tuple 和 Dict 里。
- 在函数调用处 `target_func(*args, **kwargs)` -> 星号的作用是 **「解包」**。把 Tuple 和 Dict 里的东西拆散，原封不动地喂给目标函数。
