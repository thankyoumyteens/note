# 括号匹配

[Leetcode: 20. Valid Parentheses](https://leetcode.com/problems/valid-parentheses/description/)

给定一个只包括 `(`，`)`，`{`，`}`，`[`，`]` 的字符串 s ，判断字符串是否有效。

有效字符串需满足：

1. 左括号必须用相同类型的右括号闭合。
2. 左括号必须以正确的顺序闭合。
3. 每个右括号都有一个对应的相同类型的左括号。

示例 1：

```
输入：s = "()"

输出：true
```

示例 2：

```
输入：s = "()[]{}"

输出：true
```

示例 3：

```
输入：s = "(]"

输出：false
```

示例 4：

```
输入：s = "([])"

输出：true
```

示例 5：

```
输入：s = "([)]"

输出：false
```

## 解法

遍历字符串中的每个字符:

- 如果是左括号就把它入栈
- 如果是右括号就检查栈顶的左括号能否和这个右括号匹配:
  - 如果匹配就把栈顶的左括号出栈, 继续遍历下一个字符
  - 如果不匹配就结束程序返回 false

## 代码实现

```java
import java.util.Stack;

public class ValidParentheses {
    public static boolean isValid(String s) {
        // 栈, 存储左括号
        Stack<Character> stack = new Stack<>();
        // 遍历每个字符
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '(' || c == '[' || c == '{') {
                // 如果是左括号, 入栈
                stack.push(c);
            } else {
                // 如果是右括号, 要检查栈顶的左括号能否和这个右括号匹配
                if (stack.isEmpty()) {
                    // 栈为空, 说明没有左括号可以匹配, 直接返回false
                    return false;
                }
                // 弹出栈顶的左括号
                char top = stack.pop();
                // 检查弹出的左括号是否和当前的右括号匹配
                if (c == ')' && top != '(') {
                    return false;
                }
                if (c == ']' && top != '[') {
                    return false;
                }
                if (c == '}' && top != '{') {
                    return false;
                }
                // 匹配成功, 继续遍历下一个字符
            }
        }
        // 栈为空, 说明所有的左括号都有对应的右括号
        return stack.isEmpty();
    }

    public static void main(String[] args) {
        System.out.println(isValid("([()])")); // true
        System.out.println(isValid("([)]")); // false
        System.out.println(isValid("((()))")); // true
    }
}
```
