# 异步执行

核心方法

| 方法                             | 作用                                                       |
| -------------------------------- | ---------------------------------------------------------- |
| `subprocess.Popen.poll()`        | 检查进程是否结束，返回 `None` 表示仍在运行，否则返回返回码 |
| `subprocess.Popen.wait()`        | 等待进程结束并返回返回码（可能阻塞主程序）                 |
| `subprocess.Popen.terminate()`   | 发送终止信号（SIGTERM）给进程                              |
| `subprocess.Popen.kill()`        | 强制终止进程（发送 SIGKILL）                               |
| `subprocess.Popen.communicate()` | 等待进程结束并获取全部输出（可能阻塞，适用于小输出）       |

## 异步读取输出

```py
import subprocess

process = subprocess.Popen(
    ["ping", "-c", "5", "www.example.com"],  # Linux/macOS 示例
    # ["ping", "-n", "5", "www.google.com"],  # Windows 示例
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# 主程序继续执行
print("正在ping...")

# 异步读取输出
while True:
    # 读取一行输出（如果有）
    output = process.stdout.readline()
    if output == '' and process.poll() is not None:
        # 进程结束且没有更多输出
        break
    if output:
        print(f"Ping输出: {output.strip()}")

# 获取最终返回码
return_code = process.wait()
print(f"Ping完成，返回码: {return_code}")
```

## 使用线程异步读取输出

```py
import subprocess
import threading


def read_output(stream, callback):
    for line in iter(stream.readline, ''):
        callback(line.strip())
    stream.close()


process = subprocess.Popen(
    ["ls", "-lR", "/"],  # 递归列出根目录（示例长时间命令）
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    bufsize=1,  # 行缓冲
    universal_newlines=True
)

# 创建线程处理标准输出和错误输出
stdout_thread = threading.Thread(
    target=read_output,
    args=(process.stdout, lambda x: print(f"输出: {x}"))
)
stderr_thread = threading.Thread(
    target=read_output,
    args=(process.stderr, lambda x: print(f"错误: {x}"))
)

# 启动线程
stdout_thread.start()
stderr_thread.start()

# 主程序继续执行其他任务
print("正在后台列出文件...")
# 可以添加其他主程序逻辑...

# 等待线程和进程结束
stdout_thread.join()
stderr_thread.join()
process.wait()

print("命令执行完毕")
```
