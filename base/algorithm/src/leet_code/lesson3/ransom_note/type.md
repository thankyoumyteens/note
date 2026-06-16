# 题型识别信号

看到这些关键词：

```text
can construct
ransomNote
magazine
字符是否够用
一个字符串能否由另一个字符串组成
```

优先想到：

```text
字符计数
```

这题本质是：

```text
magazine 提供字符
ransomNote 消耗字符
如果某个字符不够用，返回 false
```

它不是映射题，不需要 HashMap 的 key/value 对应关系。因为题目只涉及小写英文字母，所以 `int[26]` 最合适。
