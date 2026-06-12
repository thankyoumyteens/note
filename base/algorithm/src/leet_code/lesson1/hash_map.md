# HashMap / HashSet 的核心用途

## HashSet：只关心「有没有」

适合问题：

```text
是否出现过？
是否重复？
是否存在某个值？
```

Java 模板：

```java
Set<Integer> set = new HashSet<>();

for (int num : nums) {
    if (set.contains(num)) {
        return true;
    }
    set.add(num);
}
```

核心：

```text
HashSet 只存 key，不存额外信息。
```

---

## HashMap：关心「某个东西对应什么」

适合问题：

```text
数字 -> 下标
字符 -> 出现次数
分组 key -> 字符串列表
```

Java 模板：

```java
Map<K, V> map = new HashMap<>();
```

常见设计：

```text
Map<Integer, Integer>：数字 -> 下标 / 次数
Map<Character, Integer>：字符 -> 次数
Map<String, List<String>>：分组 key -> 字符串列表
```
