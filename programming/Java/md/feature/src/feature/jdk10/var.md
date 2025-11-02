# 局部变量类型推断

Java 10 引入的局部变量类型推断（Local-Variable Type Inference） 是一项重要的语法简化特性，允许开发者在声明局部变量时使用关键字 var 代替具体类型，由编译器根据变量的初始化值自动推断其类型。这一特性旨在减少模板代码，提升代码可读性，同时保持 Java 强类型语言的特性。

```java
// 传统写法
String message = "Hello, Java 10";
List<String> list = new ArrayList<String>();
Map<String, Integer> map = new HashMap<>();

// 类型推断写法（var）
var msg = "Hello, Java 10"; // 推断为 String
var names = new ArrayList<String>(); // 推断为 ArrayList<String>
var counts = new HashMap<String, Integer>(); // 推断为 HashMap<String, Integer>
```
