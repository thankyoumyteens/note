# HashMap 版本

如果字符集不限定为小写英文字母，可以用 HashMap：

```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public boolean isAnagram(String s, String t) {
        if (s.length() != t.length()) {
            return false;
        }

        // key: 字符
        // value: 出现次数
        Map<Character, Integer> count = new HashMap<>();

        for (char c : s.toCharArray()) {
            count.put(c, count.getOrDefault(c, 0) + 1);
        }

        for (char c : t.toCharArray()) {
            if (!count.containsKey(c)) {
                return false;
            }

            count.put(c, count.get(c) - 1);

            if (count.get(c) == 0) {
                count.remove(c);
            }
        }

        return count.isEmpty();
    }
}
```

第一遍刷题时，LeetCode 242 推荐优先掌握 `int[26]` 版本。

## 学完后应该能讲清楚什么

你应该能讲清楚：

```text
Anagram 的本质是字符频率相同
为什么不需要关心字符顺序
int[26] 为什么可以表示小写英文字母频率
什么时候用 int[26]
什么时候用 HashMap
```

## 英文面试表达模板

```text
An anagram means two strings have the same characters with the same frequencies.

I count the frequency of each character in the first string, then subtract the frequency using the second string.

If all counts become zero, the two strings are anagrams.

If the input only contains lowercase English letters, I can use an integer array of size 26.
```

复杂度：

```text
Time complexity is O(n), where n is the length of the string.

Space complexity is O(1), because the array size is fixed at 26.
```
