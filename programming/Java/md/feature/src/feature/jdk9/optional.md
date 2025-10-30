# Optional 增强

Optional 用于处理可能为 null 的值，Java 9 新增 or()、ifPresentOrElse() 和 stream() 方法，增强了空值处理的灵活性。

## ifPresentOrElse(Consumer<? super T> action, Runnable emptyAction)

作用：若 Optional 包含值，则执行 action（消费该值）；若为空，则执行 emptyAction（空值逻辑）。

解决的问题：Java 8 中需用 isPresent() 判断后分别处理，该方法合并了两种场景，代码更简洁。

```java
Optional<String> name = Optional.ofNullable("Alice");

// 有值时打印，空值时提示
name.ifPresentOrElse(
    n -> System.out.println("Hello, " + n),
    () -> System.out.println("Name is null")
); // 输出：Hello, Alice
```

## or(Supplier<? extends Optional<? extends T>> supplier)

作用：若当前 Optional 包含值，则返回自身；若为空，则返回 supplier 提供的 Optional（支持延迟计算）。

与 orElse/orElseGet 的区别：or 返回 Optional 而非具体值，可用于链式处理。

```java
Optional<String> emptyOpt = Optional.empty();
Optional<String> defaultOpt = Optional.of("Default");

// 空值时返回默认 Optional
Optional<String> result = emptyOpt.or(() -> defaultOpt);
System.out.println(result.get()); // 输出：Default
```

## stream()

作用：将 Optional 转换为 Stream：若包含值，返回包含该值的单元素流；若为空，返回空流。

适用场景：结合 Stream 操作处理 Optional 集合，实现流畅的链式调用。

```java
List<Optional<String>> list = List.of(
    Optional.of("a"),
    Optional.empty(),
    Optional.of("b")
);

// 提取所有非空值并收集为列表
List<String> nonEmptyValues = list.stream()
    .flatMap(Optional::stream) // 将每个 Optional 转为流，再扁平化
    .collect(Collectors.toList());

System.out.println(nonEmptyValues); // 输出：[a, b]
```
