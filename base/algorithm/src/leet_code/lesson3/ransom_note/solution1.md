# 解题思路

核心变量：

```text
count[i] 表示 magazine 中某个字母剩余可用次数
```

核心顺序：

1. 先统计 magazine
2. 再遍历 ransomNote 消耗字符
3. 如果某个字符被消耗到负数，说明不够用，返回 false
4. 全部消耗成功，返回 true

代码：

```java
class Solution {
    public boolean canConstruct(String ransomNote, String magazine) {
        // count[i] 记录 magazine 中第 i 个字母的可用次数
        int[] count = new int[26];

        for (char c : magazine.toCharArray()) {
            count[c - 'a']++;
        }

        for (char c : ransomNote.toCharArray()) {
            count[c - 'a']--;

            // 某个字符不够用
            if (count[c - 'a'] < 0) {
                return false;
            }
        }

        return true;
    }
}
```

复杂度：

```text
Time: O(m + n)
Space: O(1)
```

这里 `m` 和 `n` 是两个字符串长度。`Space` 是 `O(1)`，因为数组大小固定为 26。

## 常见边界条件

```text
ransomNote 为空 -> true
magazine 为空但 ransomNote 非空 -> false
字符重复很多次
只包含小写字母
```

## 英文面试表达模板

```text
I use an integer array to count the available characters in magazine.

Then I iterate through ransomNote and consume each character.

If any character count becomes negative, it means magazine does not have enough characters, so I return false.

Otherwise, I return true.
```
