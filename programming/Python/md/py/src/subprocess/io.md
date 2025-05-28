# 控制输入输出流

## 向子进程传递输入

```py
import subprocess

# 获取ls -l命令的输出
output = subprocess.check_output(["ls", "-l"], text=True)

# 通过 input 参数把上一条命令的结果传递给下一条命令
result = subprocess.run(
    ["grep", "venv"],
    input=output,
    text=True,
    capture_output=True
)
# 输出: "drwxr-xr-x   8 root  staff  256 May 29  2024 venv"
print(result.stdout)
```

## 自定义输入输出流

```py
import subprocess

with open("output.txt", "w") as f:
    subprocess.run(["ls", "-l"], stdout=f)  # 将输出写入文件

with open("output.txt", "r") as f:
    subprocess.run(["grep", "venv"], stdin=f)  # 从文件读取输入
```

## 模拟管道

```py
import subprocess

# 等同于在 shell 中执行：ls -l | grep .py

p1 = subprocess.Popen(["ls", "-l"], stdout=subprocess.PIPE)
# 把 p1 的输出作为 p2 的输入
p2 = subprocess.Popen(["grep", ".py"], stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()  # 关闭 p1 的输出以避免资源泄漏
output, _ = p2.communicate()  # 获取最终输出
print(output.decode())
```
