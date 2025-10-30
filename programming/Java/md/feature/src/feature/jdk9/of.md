# 快速创建不可变集合

Java 9 新增了集合工厂方法，用于快速创建不可变（Immutable）集合（List、Set、Map 及其子类型）。这些方法简化了不可变集合的创建流程，相比传统方式（如 Collections.unmodifiableList()）更简洁、高效，且能在编译期保证不可变性。

通过 Java 9 工厂方法创建的不可变集合具有以下特性：

- 不可修改：创建后无法添加、删除或修改元素（调用 add()、remove() 等方法会抛出 UnsupportedOperationException）
- 线程安全：由于不可修改，可安全地在多线程环境中共享，无需额外同步
- 内存高效：内部采用优化的存储结构（如紧凑的数组实现），比传统可变集合更节省内存
- 拒绝 null 元素：创建时若包含 null，会直接抛出 NullPointerException（避免 null 引发的潜在问题）

## 不可变 List

List.of() 方法用于创建不可变列表，支持 0 至多个元素

```java
// 1. 创建空不可变列表
List<String> emptyList = List.of();

// 2. 创建包含 1 个元素的列表
List<String> singleList = List.of("Java");

// 3. 创建包含多个元素的列表
List<String> fruits = List.of("apple", "banana", "orange");
```

## 不可变 Set

Set.of() 方法用于创建不可变集合，与 List 类似，但不允许重复元素（重复会抛出 IllegalArgumentException）

```java
// 1. 空集合
Set<Integer> emptySet = Set.of();

// 2. 单个元素
Set<Integer> singleSet = Set.of(100);

// 3. 多个元素（无重复）
Set<Integer> numbers = Set.of(1, 2, 3, 4);
```

## 不可变 Map

Map 的工厂方法分为两种：

- 直接传入 “键值对”（最多支持 10 个键值对）
- 通过 Map.entry() 先创建条目，再传入 Map.ofEntries()（支持任意数量键值对）

```java
// 1. 空 Map
Map<String, Integer> emptyMap = Map.of();

// 2. 单个键值对
Map<String, Integer> singleMap = Map.of("age", 25);

// 3. 多个键值对（最多 10 个）
Map<String, String> user = Map.of(
    "name", "Alice",
    "gender", "female",
    "city", "Beijing"
);

// 4. 超过 10 个键值对：使用 Map.ofEntries()
Map<String, Integer> scores = Map.ofEntries(
    Map.entry("math", 90),
    Map.entry("english", 85),
    Map.entry("physics", 95),
    Map.entry("chemistry", 88)
    // 可继续添加更多 entry
);
```
