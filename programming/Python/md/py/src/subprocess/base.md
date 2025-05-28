# 基本用法

```py
import subprocess

# 执行命令（例如：列出当前目录文件）
subprocess.run(["ls", "-l"])  # Linux/macOS
# subprocess.run(["dir"], shell=True)  # Windows
```

## 执行命令并获取输出

```py
import subprocess

# 使用 check_output() 直接获取命令输出
output = subprocess.check_output(["ls", "-l"], text=True)
print(output)
```

## 捕获输出和错误

```py
import subprocess

result = subprocess.run(
    ["ls", "-l"],
    capture_output=True,  # 捕获标准输出和错误
    text=True  # 以文本形式返回（否则为字节）
)

print("返回码:", result.returncode)  # 0 表示成功
print("标准输出:", result.stdout)
print("错误输出:", result.stderr)
```

## 检查命令是否成功

```py
import subprocess

try:
    # check=True 表示如果命令失败（返回非零码），抛出异常
    subprocess.run(["ls", "non_existent_file"], check=True)
except subprocess.CalledProcessError as e:
    print(f"命令执行失败: {e}")
```
