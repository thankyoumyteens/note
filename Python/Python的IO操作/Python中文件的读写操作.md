# Python中文件的读写操作

# 基本操作
```python
# 打开文件, 得到文件句柄并赋值给变量
f = open("a.txt","r",encoding="utf-8")
# 通过句柄对文件操作
data=f.read()
# 关闭文件
f.close()
```

# 操作文本

open(文件名, mode, encoding='utf-8')

mode|文件存在|文件不存在|操作
-|-|-|-
r|读取内容|错误|读
w|清空内容|创建|写
a|追加内容|创建|写
r+|读写内容|错误|读写
w+|清空内容|创建|读写
a+|追加内容|创建|读写

# 操作字节

open(文件名, mode)

mode|文件存在|文件不存在|操作
-|-|-|-
rb|读取内容|错误|读
wb|清空内容|创建|写
ab|追加内容|创建|写
r+b|读写内容|错误|读写
w+b|清空内容|创建|读写
a+b|追加内容|创建|读写

# 读

* `read()`: 读取整个文件的内容
* `read(n)`: 把前n个字符或字节读出来, 如果再次读取, 会在当前位置继续往后读, 而不是从头开始读
* `readline()`: 读取一行, 每次读取出来的数据都会有一个换行符`\n`
* 循环读取
```
f = open("a.txt",mode="r",encoding="utf-8")
for line in f:
　　print(line.strip())
f.close()
```

# 写

* `write(string)`: 将string写入缓冲区
* `write(string.encode("utf-8"))`: 将string写入缓冲区(指定编码)
* `flush()`: 将缓冲区的内容写入文件

