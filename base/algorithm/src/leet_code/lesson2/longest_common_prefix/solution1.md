# 解题思路

核心思路：

```text
以第一个字符串作为基准
从第一个字符串的第 0 位开始逐个字符检查
对每个位置 i，检查所有其他字符串在 i 位置是否相同
如果某个字符串长度不够，或者字符不同，返回 first.substring(0, i)
```

核心变量：

```text
first：第一个字符串，作为基准
i：当前检查的字符位置
j：当前检查的字符串下标
c：first.charAt(i)，当前基准字符
```

关键判断：

```text
i >= strs[j].length()
strs[j].charAt(i) != c
```

只要任一条件成立，公共前缀结束。

## Java 模板

```java
class Solution {
    public String longestCommonPrefix(String[] strs) {
        // 空数组没有公共前缀
        if (strs == null || strs.length == 0) {
            return "";
        }

        // 以第一个字符串为基准
        String first = strs[0];

        for (int i = 0; i < first.length(); i++) {
            char c = first.charAt(i);

            // 检查其他字符串在位置 i 上是否也是 c
            for (int j = 1; j < strs.length; j++) {
                // 如果某个字符串长度不够，或者字符不同，返回当前已确认前缀
                if (i >= strs[j].length() || strs[j].charAt(i) != c) {
                    return first.substring(0, i);
                }
            }
        }

        // 第一个字符串全部匹配，说明它就是最长公共前缀
        return first;
    }
}
```

复杂度：

```text
Time: O(n * m)
Space: O(1)
```

其中：

```text
n = 字符串数量
m = 第一个字符串长度
```

严格来说，返回的 substring 本身会占用结果字符串空间。

## 典型题目讲解

例子：

```text
["flower", "flow", "flight"]
```

逐列比较：

```text
第 0 位：f / f / f，相同
第 1 位：l / l / l，相同
第 2 位：o / o / i，不同
```

所以返回：

```text
"fl"
```

例子：

```text
["dog", "racecar", "car"]
```

第 0 位就不同：

```text
d / r / c
```

所以返回：

```text
""
```

这题的核心判断是：

```text
公共前缀必须从第 0 位开始连续相同。
```

不是找公共子串，也不是找任意相同字符。

## 常见边界条件

```text
strs 为空数组 -> ""
只有一个字符串 -> 返回它本身
某个字符串为空 -> ""
没有公共前缀 -> ""
第一个字符串就是最短字符串 -> 可能直接返回 first
大小写敏感 -> "A" 和 "a" 不相同
```

## 英文面试表达模板

```text
I use the first string as the reference.

Then I compare each character with the character at the same position in all other strings.

If a string is too short or the character is different, I return the prefix found so far.

If all characters in the first string match, the first string is the longest common prefix.
```
