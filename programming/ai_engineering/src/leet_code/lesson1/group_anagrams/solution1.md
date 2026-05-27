# 解题思路

这题是 `Valid Anagram` 的升级版。

`Valid Anagram` 是判断两个字符串是否属于同一类。

`Group Anagrams` 是把所有属于同一类的字符串放到同一组。

关键是设计一个统一的分组 key。

对于 anagram 来说：

```text
eat
tea
ate
```

排序后都会变成：

```text
aet
```

所以可以用：

```text
排序后的字符串
```

作为 HashMap 的 key。

HashMap 设计：

```text
key：排序后的字符串
value：原始字符串列表
```

每轮做什么：

```text
1. 取出当前字符串 str
2. 把 str 转成 char[]
3. 对 char[] 排序
4. 排序后转回 String，作为 key
5. 把原始 str 加入 map.get(key) 对应的列表
6. 最后返回 map 的所有 value
```

注意：

```text
key 是排序后的字符串
value 里保存的是原始字符串
```

不要把排序后的字符串放进结果。
