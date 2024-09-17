# 字符串操作

## startswith 和 endswith

```python
# True
print('a.txt'.startswith('a.'))
# True
print('a.txt'.endswith('.txt'))
```

## 查找子串

find()搜索字符串中是否包含子串 sub, 如果包含, 则返回 sub 的索引位置, 否则返回-1。可以指定起始 start 和结束 end 的搜索位置。

index()和 find()一样, 唯一不同点在于当找不到子串时, 抛出 ValueError 错误。

```python
# 1
print('abcba'.find('b'))
# 3
print('abcba'.rfind('b'))
# 1
print('abcba'.index('b'))
# 3
print('abcba'.rindex('b'))
```

## 截取子串

```py
# bc
print('abcba'[1:3])
```

## 替换

```python
# 替换全部
print('abcba'.replace('b', '-'))
# 只替换第1个
print('abcba'.replace('b', '-', 1))
```

## 分割

```python
# ['a', 'b', 'c']
print('a,b,c'.split(','))
```

## join

```python
# 集合元素必须是字符串类型
# a,b,c
print(','.join(['a', 'b', 'c']))
```

## strip

```python
# abcba
print('   abcba   '.strip())
# bcb
print('abcba'.strip('a'))
```
