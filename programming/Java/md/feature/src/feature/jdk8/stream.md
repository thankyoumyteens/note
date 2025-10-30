# Stream

Stream（流）是处理集合（Collection）的高级抽象，它允许以声明式方式对集合进行高效的聚合操作（如过滤、映射、排序、聚合等）。Stream 并非存储数据的容器，而是对数据源（如 List、Set、数组等）的一系列操作的流水线，类似于 SQL 中的查询语句，能极大简化集合处理代码。

Stream 的使用通常分为三个步骤：

1. 创建 Stream：从数据源（集合、数组等）获取流
2. 中间操作：对 Stream 进行处理（如过滤、映射、排序），返回新的 Stream（可多个中间操作串联）
3. 终端操作：触发 Stream 执行并生成结果（如生成新的集合、计算总和），执行后 Stream 关闭，不可再使用

## 创建 Stream

```java
// 从集合创建（顺序流）
List<String> list = Arrays.asList("a", "b", "c");
Stream<String> stream1 = list.stream();

// 从集合创建（并行流）
Stream<String> parallelStream = list.parallelStream();

// 从数组创建
String[] array = {"x", "y", "z"};
Stream<String> stream2 = Arrays.stream(array);

// 直接创建（单个元素）
Stream<Integer> stream3 = Stream.of(1, 2, 3);
```

## 中间操作

中间操作返回新的 Stream，支持链式调用，常用操作包括：

| 操作       | 说明                               | 示例                                    |
| ---------- | ---------------------------------- | --------------------------------------- |
| `filter`   | 过滤元素（保留满足条件的元素）     | `stream.filter(s -> s.length() > 2)`    |
| `map`      | 转换元素（将 T 类型转为 R 类型）   | `stream.map(String::length)`            |
| `flatMap`  | 扁平化处理（将流中的容器元素展开） | `stream.flatMap(list -> list.stream())` |
| `sorted`   | 排序（自然排序或自定义比较器）     | `stream.sorted(String::compareTo)`      |
| `distinct` | 去重（基于 `equals` 方法）         | `stream.distinct()`                     |
| `limit(n)` | 限制只取前 n 个元素                | `stream.limit(3)`                       |
| `skip(n)`  | 跳过前 n 个元素                    | `stream.skip(2)`                        |

示例：

```java
List<String> words = Arrays.asList("apple", "banana", "cat", "date", "apple");

// 过滤长度>3的单词, 然后转为大写, 然后去重, 然后排序
Stream<String> processed = words.stream()
    .filter(s -> s.length() > 3)    // 保留 "apple", "banana", "date", "apple"
    .map(String::toUpperCase)       // 转为 "APPLE", "BANANA", "DATE", "APPLE"
    .distinct()                     // 去重为 "APPLE", "BANANA", "DATE"
    .sorted();                      // 排序为 "APPLE", "BANANA", "DATE"
```

## 终端操作

终端操作触发 Stream 执行并返回结果，常用操作包括：

| 操作              | 说明                                   | 示例                                                       |
| ----------------- | -------------------------------------- | ---------------------------------------------------------- |
| `forEach`         | 遍历元素（无返回值）                   | `stream.forEach(System.out::println)`                      |
| `collect`         | 收集结果为集合（如 List、Set、Map）    | `stream.collect(Collectors.toList())`                      |
| `count`           | 统计元素数量                           | `long count = stream.count()`                              |
| `sum`/`max`/`min` | 数值类型 Stream 的求和、最大值、最小值 | `int sum = intStream.sum()`                                |
| `anyMatch`        | 是否存在至少一个元素满足条件           | `boolean hasLong = stream.anyMatch(s -> s.length() > 5)`   |
| `allMatch`        | 是否所有元素满足条件                   | `boolean allShort = stream.allMatch(s -> s.length() < 10)` |
| `noneMatch`       | 是否所有元素都不满足条件               | `boolean noEmpty = stream.noneMatch(String::isEmpty)`      |
| `findFirst`       | 获取第一个元素（返回 `Optional`）      | `Optional<String> first = stream.findFirst()`              |
| `reduce`          | 聚合元素为单个结果（如求和、拼接）     | `stream.reduce("", String::concat)`                        |

示例：

```java
List<String> words = Arrays.asList("apple", "banana", "cat", "date", "apple");

// 1. 收集为List
List<String> resultList = words.stream()
    .filter(s -> s.length() > 3)
    .map(String::toUpperCase)
    .distinct()
    .sorted()
    .collect(Collectors.toList());
System.out.println(resultList); // 输出：[APPLE, BANANA, DATE]

// 2. 统计数量
long count = words.stream()
    .filter(s -> s.startsWith("a"))
    .count();
System.out.println(count); // 输出：2（"apple"出现2次）

// 3. 查找最长的单词
Optional<String> longest = words.stream()
    .max((s1, s2) -> s1.length() - s2.length());
longest.ifPresent(System.out::println); // 输出：banana（长度6）

// 4. 拼接所有单词
String joined = words.stream()
    .distinct()
    .reduce("", (s1, s2) -> s1 + "-" + s2);
System.out.println(joined); // 输出：-apple-banana-cat-date
```

## 并行流（Parallel Stream）

Stream 支持并行处理，只需将 stream() 改为 parallelStream()，底层会自动利用 Fork/Join 框架分配任务到多个线程：

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

// 并行计算总和（适合大数据量场景）
int sum = numbers.parallelStream()
    .filter(n -> n % 2 == 0) // 过滤偶数
    .mapToInt(n -> n)
    .sum();
System.out.println(sum); // 输出：30（2+4+6+8+10）
```

注意：并行流并非总是更快，小数据量场景可能因线程开销导致效率更低，需根据实际情况选择。
