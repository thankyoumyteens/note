# 方法引用

方法引用（Method Reference） 是 Lambda 表达式的一种简化形式，用于直接引用已存在的方法（包括静态方法、实例方法、构造方法等）。它的作用是进一步简化代码，当 Lambda 体仅包含一个方法调用时，方法引用可以替代 Lambda 表达式，使代码更简洁。

## 静态方法引用（ClassName::staticMethod）

引用类的静态方法，适用于 Lambda 表达式的参数直接作为静态方法的参数。

```java
// Lambda表达式：将字符串转为整数
Function<String, Integer> lambda = s -> Integer.parseInt(s);
System.out.println(lambda.apply("123")); // 输出：123

// 方法引用：替代上述Lambda
Function<String, Integer> methodRef = Integer::parseInt;
System.out.println(methodRef.apply("456")); // 输出：456
```

## 实例方法引用（对象）（object::instanceMethod）

引用某个具体对象的实例方法，适用于 Lambda 表达式的参数作为该实例方法的参数。

```java
String str = "hello";

// Lambda表达式：调用str的toUpperCase方法
Supplier<String> lambda = () -> str.toUpperCase();
System.out.println(lambda.get()); // 输出：HELLO

// 方法引用：替代上述Lambda
Supplier<String> methodRef = str::toUpperCase;
System.out.println(methodRef.get()); // 输出：HELLO
```

## 实例方法引用（类）（ClassName::instanceMethod）

引用类的任意对象的实例方法，此时 Lambda 表达式的第一个参数会作为该方法的调用者，后续参数作为方法的参数。

```java
// Lambda表达式：比较两个字符串
Comparator<String> lambda = (s1, s2) -> s1.compareTo(s2);
System.out.println(lambda.compare("a", "b")); // 输出：-1（a < b）

// 方法引用：替代上述Lambda（s1作为调用者，s2作为参数）
Comparator<String> methodRef = String::compareTo;
System.out.println(methodRef.compare("b", "a")); // 输出：1（b > a）
```

## 构造方法引用（ClassName::new）

引用类的构造方法，适用于 Lambda 表达式的参数作为构造方法的参数，返回新对象。

```java
// 无参构造方法引用（Supplier接口：无参返回对象）
Supplier<List<String>> emptyList = ArrayList::new;
System.out.println(emptyList.get().size()); // 输出：0

// 有参构造方法引用（Function接口：参数为初始容量）
Function<Integer, List<String>> listWithCapacity = ArrayList::new;
System.out.println(listWithCapacity.apply(10).size()); // 输出：0（容量10，实际元素0）
```
