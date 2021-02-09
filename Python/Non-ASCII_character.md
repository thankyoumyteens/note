# Python报错：SyntaxError: Non-ASCII character '\xe5' in file 1.py on line 6, but no encoding declared...

## 报错分析：
上述报错是由于编码格式不匹配导致程序不能识别程序中的中文导致的。Python 2默认的编码格式是ASCII，Python 3默认的编码格式是UTF-8. 因此，如果我们使用Python 2运行的Python程序中出现了中文，就需要指定编码格式为UTF-8（如果使用的是Python 3则不需要指定）.

## 解决办法：
在Python脚本的开头加上：
```python
#coding=utf-8
```
或者加上：
```python
# -*- coding: UTF-8 -*-
```
保存之后再运行就不会出现上述错误了。
