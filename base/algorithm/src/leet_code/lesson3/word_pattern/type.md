# 题型识别信号

看到这些关键词：

```text
pattern
word pattern
字符和单词对应
pattern = "abba"
s = "dog cat cat dog"
```

优先想到：

```text
双向映射
```

这题和 `205. Isomorphic Strings` 本质一样，只是映射对象从：

```text
字符 -> 字符
```

变成：

```text
字符 -> 单词
```

所以模板也类似。
