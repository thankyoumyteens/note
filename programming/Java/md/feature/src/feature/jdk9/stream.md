# Stream 增强

Stream 接口在 Java 9 中新增了 takeWhile()、dropWhile()、ofNullable() 和 iterate() 重载方法，扩展了流式处理的能力。

## takeWhile(Predicate<? super T> predicate)

作用：从流的开头开始，依次获取满足 predicate 条件的元素，直到遇到第一个不满足条件的元素为止（之后的元素全部丢弃）。

特点：类似 “从头过滤，一旦不满足就停止”，适用于有序流（如列表）的前缀筛选。

```java
List<Integer> numbers = List.of(1, 2, 3, 4, 5, 3, 2);

// 从开头获取小于 4 的元素，遇到 4 时停止
numbers.stream()
       .takeWhile(n -> n < 4)
       .forEach(System.out::print); // 输出：123
```

## dropWhile(Predicate<? super T> predicate)

作用：从流的开头开始，依次丢弃满足 predicate 条件的元素，直到遇到第一个不满足条件的元素为止（之后的所有元素全部保留）。

与 takeWhile 的关系：dropWhile 是 takeWhile 的 “反向操作”，适用于跳过前缀满足条件的元素。

```java
List<Integer> numbers = List.of(1, 2, 3, 4, 5, 3, 2);

// 从开头丢弃小于 4 的元素，遇到 4 时停止丢弃
numbers.stream()
       .dropWhile(n -> n < 4)
       .forEach(System.out::print); // 输出：4532
```

## ofNullable(T t)

作用：创建一个包含单个元素的流，若元素为 null 则返回空流（而非抛出 NullPointerException）。

解决的问题：Java 8 中 Stream.of(null) 会直接抛空指针，ofNullable 可安全处理可能为 null 的元素。

```java
String str = null;

// 安全创建流：若 str 为 null，返回空流
Stream<String> stream = Stream.ofNullable(str);
System.out.println(stream.count()); // 输出：0（而非抛异常）

// 非 null 元素正常处理
Stream<String> nonNullStream = Stream.ofNullable("hello");
nonNullStream.forEach(System.out::println); // 输出：hello
```

## iterate() 重载方法

Java 8 中 `Stream.iterate(初始值, UnaryOperator)` 用于生成无限流（需配合 `limit()` 终止）。Java 9 新增重载版本：

```java
iterate(T seed, Predicate<? super T> hasNext, UnaryOperator<T> next)
```

作用：生成有限流，规则为：从 seed 开始，每次通过 next 生成下一个元素，直到 hasNext 条件不满足时停止。

优势：无需手动用 limit() 控制流的长度，更直观。

```java
// 生成 1, 3, 5, 7（当元素 >7 时停止）
Stream.iterate(1, n -> n <= 7, n -> n + 2)
      .forEach(System.out::print); // 输出：1357
```
