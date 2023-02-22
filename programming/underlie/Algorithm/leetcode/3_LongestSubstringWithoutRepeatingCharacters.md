# Longest Substring Without Repeating Characters

Given a string, find the length of the longest substring without repeating characters.

求最长无重复子串

# 例子

```
Input: "abcabcbb"
Output: 3 
Explanation: The answer is 
"abc"
, with the length of 3. 
```

# 解

维护一个滑动窗口，窗口内的都是没有重复的字符，需要尽可能的扩大窗口的大小。

窗口的右边界就是当前遍历到的字符的位置，为了求出窗口的大小，需要一个变量left来指向滑动窗口的左边界，这样，如果当前遍历到的字符从未出现过，那么直接扩大右边界，如果之前出现过，那么就分两种情况，在或不在滑动窗口内，如果不在滑动窗口内，那么就没事，当前字符可以加进来，如果在的话，就需要先在滑动窗口内去掉这个已经出现过的字符了，为了避免将左边界一位一位向右遍历查找，可以建立一个HashMap保存每个字符和其最后出现位置之间的映射，由于HashMap已经保存了该重复字符最后出现的位置，所以直接移动left指针就可以了。

维护一个结果res，每次用出现过的窗口(left,i]的大小来更新结果res，就可以得到最终结果。left指向该无重复子串左边的起始位置的前一个，由于是前一个，所以初始化就是-1，然后遍历整个字符串，对于每一个遍历到的字符，如果该字符已经在HashMap中存在了，并且如果其索引大于left的话，那么更新left为当前映射值。然后映射值更新为当前坐标i，这样保证了left始终为当前边界的前一个位置，然后计算窗口长度的时候，直接用i-left即可，用来更新结果res。

因为一旦当前字符s\[i]在HashMap已经存在映射，说明当前的字符已经出现过了，而若m\[s\[i]]>left成立，说明之前出现过的字符在窗口内，那么如果要加上当前遍历到的这个重复的字符，就要移除之前的那个，所以让left赋值为m\[s\[i]]，由于left是窗口左边界的前一个位置，所以相当于已经移除出滑动窗口了。

```java
class Solution {
public int lengthOfLongestSubstring(String s) {
        int res = 0;
        int left = -1;
        HashMap<Character, Integer> m = new HashMap<>();
        for (int i = 0; i < s.length(); ++i) {
            // s[i]
            char c = s.charAt(i);
            if (m.containsKey(c) && m.get(c) > left) {
                left = m.get(c);  
            }
            m.put(c, i);
            res = Math.max(res, i - left);            
        }
        return res;
    }
}
```
