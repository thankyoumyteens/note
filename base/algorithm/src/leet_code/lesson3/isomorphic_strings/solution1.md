# 解题思路

核心变量：

```text
sToT：记录 s 中字符 -> t 中字符
tToS：记录 t 中字符 -> s 中字符
```

核心顺序：

1. 长度不同直接 false
2. 同时遍历 s 和 t
3. 检查 sToT 是否冲突
4. 检查 tToS 是否冲突
5. 两边都不冲突，记录映射

代码：

```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public boolean isIsomorphic(String s, String t) {
        if (s.length() != t.length()) {
            return false;
        }

        Map<Character, Character> sToT = new HashMap<>();
        Map<Character, Character> tToS = new HashMap<>();

        for (int i = 0; i < s.length(); i++) {
            char a = s.charAt(i);
            char b = t.charAt(i);

            // a 已经映射过，但不是映射到 b，说明冲突
            if (sToT.containsKey(a) && sToT.get(a) != b) {
                return false;
            }

            // b 已经被别的字符映射过，也说明冲突
            if (tToS.containsKey(b) && tToS.get(b) != a) {
                return false;
            }

            sToT.put(a, b);
            tToS.put(b, a);
        }

        return true;
    }
}
```

复杂度：

```text
Time: O(n)
Space: O(k)
```

`k` 是不同字符的数量。

## 常见边界条件

```text
长度不同
同一个字符映射到不同字符
不同字符映射到同一个字符
重复字符
单字符字符串
```

## 英文面试表达模板

```text
I use two hash maps to maintain a one-to-one mapping.

The first map stores the mapping from characters in s to characters in t.

The second map stores the reverse mapping from t to s.

If either direction has a conflict, I return false.

Otherwise, the two strings are isomorphic.
```
