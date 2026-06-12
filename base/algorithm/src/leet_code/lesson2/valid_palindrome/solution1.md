# 解题思路

核心思路：

```text
left 指向字符串左侧
right 指向字符串右侧

每轮先跳过左右两边的非字母数字字符
然后比较两个字符的小写形式
如果不同，返回 false
如果相同，left++，right--
```

核心变量：

```text
left：左指针
right：右指针
Character.isLetterOrDigit：判断是否字母或数字
Character.toLowerCase：统一大小写
```

## Java 模板

```java
class Solution {
    public boolean isPalindrome(String s) {
        int left = 0;
        int right = s.length() - 1;

        while (left < right) {
            // 跳过左边的非字母数字字符
            while (left < right && !Character.isLetterOrDigit(s.charAt(left))) {
                left++;
            }

            // 跳过右边的非字母数字字符
            while (left < right && !Character.isLetterOrDigit(s.charAt(right))) {
                right--;
            }

            // 比较时统一转成小写
            char l = Character.toLowerCase(s.charAt(left));
            char r = Character.toLowerCase(s.charAt(right));

            if (l != r) {
                return false;
            }

            left++;
            right--;
        }

        return true;
    }
}
```

复杂度：

```text
Time: O(n)
Space: O(1)
```

## 典型题目讲解

例子：

```text
"A man, a plan, a canal: Panama"
```

忽略空格、逗号、冒号，并统一小写后，相当于：

```text
"amanaplanacanalpanama"
```

它正反一致，所以返回：

```text
true
```

例子：

```text
"race a car"
```

忽略空格后：

```text
"raceacar"
```

不是回文，返回：

```text
false
```

这题最容易错的地方不是双指针，而是：

```text
忘记跳过非字母数字字符
忘记统一大小写
跳过字符时没有 left < right，导致越界
```

## 常见边界条件

```text
空字符串 -> true
只有一个字符 -> true
全是标点符号 -> true
大小写混合 -> 需要统一小写
包含数字 -> 数字也要参与比较
包含空格和标点 -> 跳过
```

典型边界：

```text
" " -> true
"0P" -> false
".," -> true
```

## 英文面试表达模板

```text
I use two pointers, one from the beginning and one from the end.

I skip non-alphanumeric characters on both sides.

Then I compare the remaining characters in lowercase.

If any pair is different, I return false.

Otherwise, the string is a valid palindrome.
```
