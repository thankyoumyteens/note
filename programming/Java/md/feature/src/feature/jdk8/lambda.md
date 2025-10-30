# lambda 表达式

Lambda 表达式 是一种简洁的匿名函数，用于简化函数式接口的实现。它极大地简化了匿名内部类的写法，尤其适合与 Stream、Optional 等 API 配合，大幅提升集合处理、异步编程等场景的开发效率。

## 示例: Comparator 接口

传统写法：

```java
Collections.sort(list, new Comparator<String>() {
    @Override
    public int compare(String s1, String s2) {
        return s1.compareTo(s2);
    }
});
```

Lambda 简化后：

```java
Collections.sort(list, (s1, s2) -> s1.compareTo(s2));
```
