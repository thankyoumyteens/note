# 基本使用

```py
import threading
import time

# 定义线程要执行的函数
def print_numbers():
    for i in range(5):
        time.sleep(1)  # 模拟耗时操作
        print(f"数字: {i}")

# 创建线程对象
thread = threading.Thread(target=print_numbers)
# 启动线程
thread.start()

# 主线程继续执行其他操作
for i in range(3):
    time.sleep(1.5)
    print("主线程工作中...")

# 等待子线程完成
thread.join()
print("所有工作完成")
```

## 线程传参

可以通过 args 和 kwargs 参数向线程函数传递参数

```py
import threading
import time


def greet(name, times):
    for i in range(times):
        time.sleep(1)
        print(f"Hello, {name}! 第{i + 1}次")


# 通过 args 创建
thread = threading.Thread(target=greet, args=("Alice", 3))
# 通过 kwargs 创建
# thread = threading.Thread(target=greet, kwargs={"name": "Alice", "times": 3})

thread.start()
thread.join()
```
