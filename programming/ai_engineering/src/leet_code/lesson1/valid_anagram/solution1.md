# 解题思路

这题不是比较字符顺序，而是比较字符频率。

例如：

```text
s = "anagram"
t = "nagaram"
```

虽然顺序不同，但每个字符出现次数相同，所以是 anagram。

可以用两种方式：

```text
1. HashMap<Character, Integer>
2. int[26]
```
