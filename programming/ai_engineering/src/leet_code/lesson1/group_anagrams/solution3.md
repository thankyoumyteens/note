# 熟练后写法

```java
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();

        for (String str : strs) {
            char[] chars = str.toCharArray();
            Arrays.sort(chars);
            String key = new String(chars);

            map.computeIfAbsent(key, k -> new ArrayList<>()).add(str);
        }

        return new ArrayList<>(map.values());
    }
}
```

第一遍建议用普通写法，因为更容易理解：

```text
没有这个 key，就创建列表；
有这个 key，就加入列表。
```

## 学完后应该能讲清楚什么

你应该能讲清楚：

```text
为什么 anagram 排序后会得到相同 key
HashMap 的 key 为什么是排序后的字符串
HashMap 的 value 为什么是 List<String>
为什么结果返回 map.values()
为什么加入列表的是原始字符串，而不是排序后的 key
```

---

## 英文面试表达模板

```text
The key idea is that anagrams become the same string after sorting their characters.

I use the sorted string as the key in a hash map.

The value is a list of original strings that belong to the same anagram group.

For each string, I compute its sorted key and add the original string to the corresponding list.

Finally, I return all the values from the hash map.
```

复杂度：

```text
Let n be the number of strings, and k be the maximum length of a string.

For each string, sorting takes O(k log k), so the total time complexity is O(n * k log k).

The space complexity is O(n * k), because we store all strings in the hash map.
```
