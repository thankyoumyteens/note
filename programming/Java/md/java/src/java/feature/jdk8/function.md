# 函数式接口

函数式接口（Functional Interface） 是指只包含一个抽象方法的接口（可以包含多个默认方法(default 修饰)或静态方法(static 修饰)）。它的核心作用是为 Lambda 表达式 和 方法引用 提供类型支持，是函数式编程在 Java 中的基础。

函数式接口的特点:

- 单一抽象方法（SAM, Single Abstract Method）：接口中只能有一个未实现的抽象方法（默认方法和静态方法不影响）
- 可被 Lambda 表达式实现：函数式接口可以通过 Lambda 表达式直接实例化，无需编写匿名内部类
- 注解标识：可以用 `@FunctionalInterface` 注解标记（非强制，但推荐），这样的话编译器就会检查是否符合函数式接口规范（若有多个抽象方法则报错）

Java 8 的 java.util.function 包中定义了大量常用的函数式接口，覆盖了大多数函数式编程场景

| 接口                | 方法                     | 功能                                    |
| ------------------- | ------------------------ | --------------------------------------- |
| `Consumer<T>`       | `void accept(T t)`       | 接收一个参数，无返回值（消费数据）      |
| `Supplier<T>`       | `T get()`                | 无参数，返回一个结果（提供数据）        |
| `Function<T, R>`    | `R apply(T t)`           | 接收 T 类型参数，返回 R 类型结果        |
| `Predicate<T>`      | `boolean test(T t)`      | 接收 T 类型参数，返回布尔值（条件判断） |
| `BiFunction<T,U,R>` | `R apply(T t, U u)`      | 接收两个参数，返回一个结果              |
| `BiConsumer<T,U>`   | `void accept(T t, U u)`  | 接收两个参数，无返回值                  |
| `BiPredicate<T,U>`  | `boolean test(T t, U u)` | 接收两个参数，返回布尔值                |
