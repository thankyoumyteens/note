# 准备

准备(Preparation)阶段是是连接阶段(Linking)的第二步，它是为类中的静态变量分配内存并设置初始零值的阶段。在准备阶段进行内存分配的仅包括类变量，而不包括实例变量，实例变量将会在对象实例化时随着对象一起分配在 Java 堆中。

类变量只在理论上是存储于方法区中的。在 JDK 7 之前，HotSpot 使用永久代来实现方法区，类变量存储在永久代中。但从 JDK 7 开始，类变量改为存放在 Java 堆中。

## 初始零值

假设一个类变量的定义为：

```java
public static int value = 123;
```

那变量 value 在准备阶段过后的初始值为 0 而不是 123，因为这时尚未开始执行任何 Java 方法，而把 value 赋值为 123 的 putstatic 指令是程序被编译后，存放于类构造器`<clinit>()`方法之中的，所以把 value 赋值为 123 的动作要到类的初始化阶段才会被执行。

基本数据类型的零值：

| 数据类型  | 零值   |
| --------- | ------ |
| int       | 0      |
| long      | 0L     |
| short     | 0      |
| char      | \u0000 |
| byte      | 0      |
| boolean   | false  |
| float     | 0.0f   |
| double    | 0.0d   |
| reference | null   |

## 特殊情况

如果字段的属性表中存在 ConstantValue 属性，那在准备阶段变量值就会被初始化为 ConstantValue 属性所指定的初始值。

静态常量(使用 static+final 修饰)，且使用字面量显式赋值时，javac 在编译时就会为它生成 ConstantValue 属性。

```java
public class LinkingTest {
    // 准备阶段赋值为100
    public static final int num0 = 100;
    // 准备阶段赋值为"helloworld"
    public static final String s0 = "helloworld";

    // 准备阶段赋值为0。没有final修饰，所以设置为零值
    private static int num1 = 100;
    // 准备阶段赋值为null。使用了String的构造方法，所以设置为零值
    public static final String s1 = new String("helloworld1");
}
```

## ConstantValue 属性

ConstantValue 属性的作用是通知虚拟机自动为静态变量赋值。只有被 static 关键字修饰的变量(类变量)才可以使用这项属性。

对于类变量，有两种赋值方式可以选择：

1. 在类构造器`<clinit>()`方法中赋值
2. 使用 ConstantValue 属性，在准备阶段赋值

目前 Oracle 公司实现的 Javac 编译器的选择是，如果同时使用 final 和 static 来修饰一个变量，并且这个变量的数据类型是基本类型或者 java.lang.String 的话，就将会生成 ConstantValue 属性来进行初始化。如果这个变量没有被 final 修饰，或者并非基本类型及字符串，则会在`<clinit>()`方法中进行初始化。

ConstantValue 属性结构：

| 类型 | 名称                 | 数量 |
| ---- | -------------------- | ---- |
| u2   | attribute_name_index | 1    |
| u4   | attribute_length     | 1    |
| u2   | constantvalue_index  | 1    |

ConstantValue 属性是一个定长属性，它的 attribute_length 数据项值必须固定为 2。constantvalue_index 数据项代表了常量池中一个字面量常量的引用，这个字面量可以是 CONSTANT_Long_info、CONSTANT_Float_info、CONSTANT_Double_info、CONSTANT_Integer_info 和 CONSTANT_String_info 常量中的一种。
