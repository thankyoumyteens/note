# LocalVariableTable 属性

LocalVariableTable 属性用于描述栈帧中局部变量表的变量与 Java 源码中定义的变量之间的关系, 它也不是运行时必需的属性, 但默认会生成到 Class 文件之中。如果没有生成这项属性, 最大的影响就是当其他人引用这个方法时, 所有的参数名称都将会丢失, 比如 IDE 将会使用诸如 arg0、arg1 之类的占位符代替原有的参数名, 这对程序运行没有影响, 但是会对代码编写带来较大不便, 而且在调试期间无法根据参数名称从上下文中获得参数值。

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

start_pc 和 length 属性分别代表了这个局部变量的生命周期开始的字节码偏移量及其作用范围覆盖的长度, 两者结合起来就是这个局部变量在字节码之中的作用域范围。

name_index 和 descriptor_index 都是指向常量池中 CONSTANT_Utf8_info 型常量的索引, 分别代表了局部变量的名称以及这个局部变量的描述符。

index 是这个局部变量在栈帧的局部变量表中变量槽的位置。当这个变量数据类型是 64 位类型时, 它占用的变量槽为 index 和 index+1 两个。

---

![](../../img/class_file8.png)

Code 属性表中的第二个属性: attribute_name_index 为`0x000B`, 指向常量池中索引为 11 的值`LocalVariableTable`。attribute_length 为`0x0000000C`, local_variable_table_length 为`0x0001`。local_variable_info 中的 start_pc 为`0x0000`, length 为`0x0005`, name_index 为`0x000C`, 指向常量池中索引为 12 的值`this`, descriptor_index 为`0x000D`, 指向常量池中索引为 13 的值`LClassFileDemo;`, index 为`0x0000`。

使用 javap -verbose ClassFileDemo.class 命令解析 class 文件:

![](../../img/javap7.png)
