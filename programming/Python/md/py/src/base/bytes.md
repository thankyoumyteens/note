# bytes 操作

在 Python 中，`bytes` 类型用于表示不可变的字节序列，常用于处理二进制数据，如文件读写、网络传输等场景。

## 创建 bytes 对象

## 直接定义

使用 `b` 前缀加字符串

```python
b1 = b"hello"  # 只能包含 ASCII 字符
b2 = b'\x68\x65\x6c\x6c\x6f'  # 十六进制表示（等价于 b"hello"）
```

## 通过 `bytes()` 构造函数

```python
# 从字符串创建（需指定编码）
b3 = bytes("你好", encoding="utf-8")

# 从整数序列创建（每个元素需在 0-255 范围内）
b4 = bytes([104, 101, 108, 108, 111])  # 等价于 b"hello"

# 创建指定长度的空字节序列（填充 0）
b5 = bytes(5)  # b'\x00\x00\x00\x00\x00'
```

## 基本操作

```python
b = b"hello"

# 通过索引获取单个字节（返回整数）
print(b[0])  # 104（对应字符 'h' 的 ASCII 码）

# 切片操作
print(b[1:4])  # b'ell'

# 拼接与重复
print(b"hello" + b" world")  # b'hello world'
print(b"a" * 3)  # b'aaa'

# 长度计算
print(len(b"hello"))  # 5
```

### 常用方法

```python
b = b"hello world"

# 查找子串
print(b.find(b"world"))  # 6（找到返回索引）
print(b.find(b"python"))  # -1（未找到返回 -1）

# 判断前缀/后缀
print(b.startswith(b"he"))  # True
print(b.endswith(b"d"))     # True

# 分割
print(b"a,b,c".split(b","))  # [b'a', b'b', b'c']

# 转换为十六进制字符串
print(b"hello".hex())  # "68656c6c6f"

# 从十六进制字符串创建 bytes
print(bytes.fromhex("68656c6c6f"))  # b'hello'
```

## 与其他类型的转换

### bytes 和 str

```python
s = "你好"
b = s.encode("utf-8")  # 字符串 -> bytes
s2 = b.decode("utf-8")  # bytes -> 字符串
```

### bytes 和 bytearray

bytearray 是可变版本的字节序列

```python
b = b"hello"
ba = bytearray(b)  # 转换为可变类型
ba[0] = 65  # 修改第一个字节（65 对应 'A'）
print(ba)  # bytearray(b'Aello')
```
