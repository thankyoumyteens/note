# 普通写法

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        // key: 排序后的字符串
        // value: 属于同一组 anagram 的原始字符串列表
        Map<String, List<String>> map = new HashMap<>();

        for (String str : strs) {
            // 将字符串转成字符数组，方便排序
            char[] chars = str.toCharArray();
            Arrays.sort(chars);

            // 排序后的字符串作为分组 key
            String key = new String(chars);

            // 如果这个 key 第一次出现，先创建一个列表
            if (!map.containsKey(key)) {
                map.put(key, new ArrayList<>());
            }

            // 注意：加入的是原始字符串 str，不是 key
            map.get(key).add(str);
        }

        // 返回所有分组
        return new ArrayList<>(map.values());
    }
}
```
