# 集合增强

List，Set，Map 提供了静态方法 copyOf() 返回入参集合的一个不可变拷贝

```java
List<Integer> list = List.of(1, 2, 3, 4, 5);

List<Integer> copy = List.copyOf(list);
```
