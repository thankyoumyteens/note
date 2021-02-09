# python中str和byte相互转化
```python
a = b"Hello, world!"   # bytes object
b = "Hello, world!"    # str object
```

# 字符串转字节  str --> bytes
```python
print(str.encode(b))  # 默认 encoding="utf-8"
print(bytes(b, encoding="utf8"))
print(b.encode())      # 默认 encoding="utf-8"
```

# 字节转字符串  bytes --> str
```python
print(bytes.decode(a))   # 默认encoding="utf-8"
print(str(a, encoding="utf-8"))
print(a.decode())       # 默认 encoding="utf-8"
```
