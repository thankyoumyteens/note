# String 增强

Java 12（JEP 325）引入了对 String 类的几项改进，主要包括两个新方法和对 JVM Constants API 的支持。这些增强旨在提升字符串处理的便利性和性能。下面详细列出主要变化：

## indent 方法

```java
indent(int n)
```

根据参数 `n` 的值调整字符串每一行的缩进（添加或移除空格），并规范化行结束符（统一为 `\n`）。如果 `n > 0`，则添加缩进；如果 `n < 0`，则移除相应数量的空格（不会移除非空格字符）。

```java
String str = "Welcome\nto Java 12!";
System.out.println(str.indent(4));
// 输出：
//     Welcome
//     to Java 12!
```

注意：如果 `n` 为负值且空格不足，则仅移除现有空格。

## transform 方法

```java
transform(UnaryOperator<T> operator)
```

接受一个函数式接口 `UnaryOperator`，将当前字符串作为输入应用到该函数，并返回函数的输出结果。支持链式调用，允许灵活转换字符串。

```java
String text = "hello";
String reversed = text.transform(s -> new StringBuilder(s).reverse().toString());  // 输出："olleh"
```

## 实现新接口：Constable 和 ConstantDesc

String 类实现了这两个接口，支持 JVM Constants API（JEP 334），允许字符串作为常量池中的可加载常量。主要用于低级 JVM 操作和常量优化，开发者很少直接调用，但提升了 String 在常量池中的效率。
