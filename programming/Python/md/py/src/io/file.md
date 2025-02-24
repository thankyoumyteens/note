# 文件操作

## 常规操作

```python
f = open('a.txt', 'r', encoding='utf-8')
for line in f:
    print(line, end='')
f.close()
```

## 使用 with 自动释放资源

```python
with open('a.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line, end='')
```

# 通过 pathlib 打开文件

```python
from pathlib import Path

src_path = Path('a.txt')

with src_path.open('r', encoding='utf-8') as f:
    for line in f:
        print(line, end='')
```

## 打开文本文件

```python
open(文件名, mode, encoding='utf-8')
```

| mode | 文件存在 | 文件不存在 | 操作 |
| ---- | -------- | ---------- | ---- |
| r    | 读取内容 | 错误       | 读   |
| w    | 清空内容 | 创建       | 写   |
| a    | 追加内容 | 创建       | 写   |
| r+   | 读写内容 | 错误       | 读写 |
| w+   | 清空内容 | 创建       | 读写 |
| a+   | 追加内容 | 创建       | 读写 |

## 打开二进制文件

```python
open(文件名, mode)
```

| mode | 文件存在 | 文件不存在 | 操作 |
| ---- | -------- | ---------- | ---- |
| rb   | 读取内容 | 错误       | 读   |
| wb   | 清空内容 | 创建       | 写   |
| ab   | 追加内容 | 创建       | 写   |
| r+b  | 读写内容 | 错误       | 读写 |
| w+b  | 清空内容 | 创建       | 读写 |
| a+b  | 追加内容 | 创建       | 读写 |

## 读文件

- `read()`: 读取整个文件的内容
- `read(n)`: 把前 n 个字符或字节读出来, 如果再次读取, 会在当前位置继续往后读, 而不是从头开始读
- `readline()`: 读取一行, 每次读取出来的数据都会有一个换行符`\n`

## 写文件

- `write(string)`: 将 string 写入缓冲区
- `write(string.encode('utf-8'))`: 将 string 写入缓冲区(指定编码)
- `flush()`: 将缓冲区的内容写入文件

## 写入字节

```py
import sys

# Hello World!
file_content = [
    0x48,
    0x65,
    0x6C,
    0x6C,
    0x6F,
    0x2C,
    0x20,
    0x57,
    0x6F,
    0x72,
    0x6C,
    0x64,
    0x21,
]

with open('test', 'wb') as f:
    for byte in file_content:
        # int.to_bytes: 把一个整数转换为指定长度的字节序列
        # sys.byteorder: 获取系统是大端还是小端
        f.write(byte.to_bytes(1, byteorder=sys.byteorder))
    f.flush()
```
