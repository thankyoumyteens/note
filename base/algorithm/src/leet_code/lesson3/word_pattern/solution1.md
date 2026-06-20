# 解题思路

核心变量：

```text
charToWord：pattern 字符 -> 单词
wordToChar：单词 -> pattern 字符
```

核心顺序：

1. 把 s 按空格拆成 words
2. pattern 长度和 words 数量不同，直接 false
3. 同时遍历 pattern 和 words
4. 检查 char -> word 是否冲突
5. 检查 word -> char 是否冲突
6. 两边都不冲突，记录映射

代码：

```java
import java.util.HashMap;
import java.util.Map;

class Solution {
    public boolean wordPattern(String pattern, String s) {
        String[] words = s.split(" ");

        if (pattern.length() != words.length) {
            return false;
        }

        Map<Character, String> charToWord = new HashMap<>();
        Map<String, Character> wordToChar = new HashMap<>();

        for (int i = 0; i < pattern.length(); i++) {
            char c = pattern.charAt(i);
            String word = words[i];

            // c 已经映射过，但不是映射到当前 word
            if (charToWord.containsKey(c) && !charToWord.get(c).equals(word)) {
                return false;
            }

            // word 已经被别的字符映射过
            if (wordToChar.containsKey(word) && wordToChar.get(word) != c) {
                return false;
            }

            charToWord.put(c, word);
            wordToChar.put(word, c);
        }

        return true;
    }
}
```

复杂度：

```text
Time: O(n)
Space: O(n)
```

`n` 是单词数量。

## 常见边界条件

```text
pattern 长度和 words 数量不同
同一个 pattern 字符对应不同单词
不同 pattern 字符对应同一个单词
重复单词
重复 pattern 字符
```

## 英文面试表达模板

```text
This problem is similar to isomorphic strings.

I use two hash maps to keep a one-to-one mapping between pattern characters and words.

One map stores character to word, and the other stores word to character.

If either mapping has a conflict, I return false.

Otherwise, the pattern matches the string.
```
