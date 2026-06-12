# 数组计数版本

如果题目限定只有小写英文字母，优先用 `int[26]`，更简单高效。

数组计数设计：

```text
count[0] 表示 'a' 的次数
count[1] 表示 'b' 的次数
...
count[25] 表示 'z' 的次数
```

每轮做什么：

```text
1. 如果 s 和 t 长度不同，直接 false
2. 遍历 s，让对应字符计数 +1
3. 遍历 t，让对应字符计数 -1
4. 最后检查所有计数是否为 0
```

如果全是 0，说明两个字符串字符频率完全一致。

## Java 模板：数组计数版本

```java
class Solution {
    public boolean isAnagram(String s, String t) {
        // 长度不同，不可能是 anagram
        if (s.length() != t.length()) {
            return false;
        }

        // 只适用于小写英文字母 a-z
        int[] count = new int[26];

        // 统计 s 中每个字符出现次数
        for (char c : s.toCharArray()) {
            count[c - 'a']++;
        }

        // 用 t 中的字符抵消
        for (char c : t.toCharArray()) {
            count[c - 'a']--;
        }

        // 如果所有计数都回到 0，说明字符频率完全相同
        for (int num : count) {
            if (num != 0) {
                return false;
            }
        }

        return true;
    }
}
```
