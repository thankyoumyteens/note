# 3种字符串对象类型

- str表示Unicode文本(8位的和更宽的)
- bytes表示二进制数据
- bytearray, 是一种可变的bytes类型

# 字符串类型的判断

```python
b = type(text) is bytes
b = type(text) is str
```

# bytes和str互转

- `str.encode()` 把一个str转换为其bytes形式
- `bytes.decode()` 把bytes转换为str形式
