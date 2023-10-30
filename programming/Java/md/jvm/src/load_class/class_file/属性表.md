# 属性表

Class 文件、字段表、方法表都可以携带自己的属性表集合(attributes)，用来存储它们自己的信息。

对于每一个属性，它的名称都要从常量池中引用一个 CONSTANT_Utf8_info 类型的常量来表示，而属性值的结构则是完全自定义的，只需要通过一个 u4 的长度属性去说明属性值所占用的位数即可。

## 属性表的通用结构

| 类型 | 名称                 | 数量             |
| ---- | -------------------- | ---------------- |
| u2   | attribute_name_index | 1                |
| u4   | attribute_length     | 1                |
| u1   | 各属性自定义         | attribute_length |

## Code 属性表

Code 属性表是一种用来存储方法体的属性表。它包含了方法的指令、局部变量表、操作数栈、异常处理器等信息。

| 类型           | 名称                   | 数量                   |
| -------------- | ---------------------- | ---------------------- |
| u2             | attribute_name_index   | 1                      |
| u4             | attribute_length       | 1                      |
| u2             | max_stack              | 1                      |
| u2             | max_locals             | 1                      |
| u4             | code_length            | 1                      |
| u1             | code                   | code_length            |
| u2             | exception_table_length | 1                      |
| exception_info | exception_table        | exception_table_length |
| u2             | attributes_count       | 1                      |
| attribute_info | attributes             | attributes_count       |

- attribute_name_index 是一项指向常量池中 CONSTANT_Utf8_info 型常量的索引，此常量值固定为 Code
- attribute_length 表示属性值的长度，由于 attribute_name_index 与 attribute_length 一共为 6 个字节，所以属性值的长度固定为整个属性表长度减去 6 个字节
- max_stack 代表了栈帧中操作数栈的最大深度。在方法执行的任意时刻，操作数栈都不会超过这个深度。虚拟机运行的时候需要根据这个值来分配栈帧中的操作数栈深度
- max_locals 代表了局部变量表所需的存储空间
- code_length 代表字节码指令长度
- code 用于存储字节码指令。每个指令是一个 u1 类型的单字节，当虚拟机读取到 code 中的一个字节码时，就可以找出这个字节码代表的是什么指令，并且可以知道这条指令后面是否需要跟随参数，以及后续的参数应当如何解析。一个 u1 类型一共可以表达 256 条指令，目前已经定义了大约 200 条指令

---

```java
public class ClassFileDemo {
    int num;

    public int getNum() {
        return this.num;
    }
}
```

字节码文件内容:

![](../../img/class_file7.png)

attribute_name_index 为`0x0009`，指向常量池中索引为 9 的值`Code`，说明此属性是方法的字节码描述。attribute_length 为`0x0000002F`，即十进制的 47。

max_stack 的值为`0x0001`，max_locals 的值也是`0x0001`。code_length 为`0x00000005`，所以接下来的 5 个字节`0x2AB70001B1`就是方法的字节码指令。

- `0x2A`表示指令`aload_0`
- `0xB7`表示指令`invokespecial`
- `0x0001`是指令`invokespecial`的操作数，指向常量池中的一个 CONSTANT_Methodref_info 类型的常量，即此方法的符号引用
- `0xB1`表示指令`return`

exception_table_length 为`0x0000`，异常表为空。

接着是 attributes_count`0x0002`，表示 Code 属性表中又包含了两个属性。

使用 javap -verbose ClassFileDemo.class 命令解析 class 文件：

![](../../img/javap6.png)

## LineNumberTable 属性

LineNumberTable 属性用于描述 Java 源码行号与字节码行号之间的对应关系。它不是运行时必需的属性，但默认会生成到 Class 文件之中。如果选择不生成 LineNumberTable 属性，当抛出异常时，堆栈中将不会显示出错的行号，并且在调试程序的时候，也无法按照源码行来设置断点。

| 类型             | 名称                     | 数量                     |
| ---------------- | ------------------------ | ------------------------ |
| u2               | attribute_name_index     | 1                        |
| u4               | attribute_length         | 1                        |
| u2               | line_number_table_length | 1                        |
| line_number_info | line_number_table        | line_number_table_length |

line_number_table 是一个数量为 line_number_table_length、类型为 line_number_info 的集合，line_number_info 包含 start_pc 和 line_number 两个 u2 类型的数据项，前者是字节码行号，后者是 Java 源码行号。

## LocalVariableTable 属性

LocalVariableTable 属性用于描述栈帧中局部变量表的变量与 Java 源码中定义的变量之间的关系，它也不是运行时必需的属性，但默认会生成到 Class 文件之中。如果没有生成这项属性，最大的影响就是当其他人引用这个方法时，所有的参数名称都将会丢失，比如 IDE 将会使用诸如 arg0、arg1 之类的占位符代替原有的参数名，这对程序运行没有影响，但是会对代码编写带来较大不便，而且在调试期间无法根据参数名称从上下文中获得参数值。

| 类型                | 名称                        | 数量                        |
| ------------------- | --------------------------- | --------------------------- |
| u2                  | attribute_name_index        | 1                           |
| u4                  | attribute_length            | 1                           |
| u2                  | local_variable_table_length | 1                           |
| local_variable_info | local_variable_table        | local_variable_table_length |

### local_variable_info 结构

| 类型 | 名称             | 数量 |
| ---- | ---------------- | ---- |
| u2   | start_pc         | 1    |
| u2   | length           | 1    |
| u2   | name_index       | 1    |
| u2   | descriptor_index | 1    |
| u2   | index            | 1    |

start_pc 和 length 属性分别代表了这个局部变量的生命周期开始的字节码偏移量及其作用范围覆盖的长度，两者结合起来就是这个局部变量在字节码之中的作用域范围。

name_index 和 descriptor_index 都是指向常量池中 CONSTANT_Utf8_info 型常量的索引，分别代表了局部变量的名称以及这个局部变量的描述符。

index 是这个局部变量在栈帧的局部变量表中变量槽的位置。当这个变量数据类型是 64 位类型时，它占用的变量槽为 index 和 index+1 两个。

---

![](../../img/class_file8.png)

Code 属性表中的第一个属性：attribute_name_index 为`0x000A`，指向常量池中索引为 10 的值`LineNumberTable`。attribute_length 为`0x00000006`，line_number_table_length 为`0x0001`。line_number_info 中的 start_pc 为`0x0000`，line_number 为`0x0001`。

Code 属性表中的第二个属性：attribute_name_index 为`0x000B`，指向常量池中索引为 11 的值`LocalVariableTable`。attribute_length 为`0x0000000C`，local_variable_table_length 为`0x0001`。local_variable_info 中的 start_pc 为`0x0000`，length 为`0x0005`，name_index 为`0x000C`，指向常量池中索引为 12 的值`this`，descriptor_index 为`0x000D`，指向常量池中索引为 13 的值`LClassFileDemo;`，index 为`0x0000`。

使用 javap -verbose ClassFileDemo.class 命令解析 class 文件：

![](../../img/javap7.png)

## SourceFile 属性

SourceFile 属性用于记录生成这个 Class 文件的源码文件名称，这个属性也是可选的。在 Java 中，对于大多数的类来说，类名和文件名是一致的，但是有一些特殊情况(如内部类)例外。如果不生成这项属性，当抛出异常时，堆栈中将不会显示出错代码所属的文件名。

| 类型 | 名称                 | 数量 |
| ---- | -------------------- | ---- |
| u2   | attribute_name_index | 1    |
| u4   | attribute_length     | 1    |
| u2   | sourcefile_index     | 1    |

sourcefile_index 数据项是指向常量池中 CONSTANT_Utf8_info 型常量的索引，常量值是源码文件的文件名。

---

![](../../img/class_file10.png)

方法表结束后，紧接着的 attributes_count`0x0001`，表示这个 Class 文件有 1 个附加属性。

attribute_name_index 为`0x0010`，指向常量池中索引为 16 的值`SourceFile`，说明此属性是这个 Class 文件的源码文件名称。attribute_length 为`0x00000002`。sourcefile_index 为`0x0011`，指向常量池中索引为 17 的值`ClassFileDemo.java`。

使用 javap -verbose ClassFileDemo.class 命令解析 class 文件：

![](../../img/javap9.png)
