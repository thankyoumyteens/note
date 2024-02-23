# 类型转换指令

类型转换指令可以将两种不同的数值类型相互转换。

Java 虚拟机直接支持（即转换时无须显式的转换指令）以下数值类型的宽化类型转换（WideningNumeric Conversion, 即小范围类型向大范围类型的安全转换）:

- int 类型到 long、float 或者 double 类型
- long 类型到 float、double 类型
- float 类型到 double 类型

与之相对的, 处理窄化类型转换（Narrowing Numeric Conversion）时, 就必须显式地使用转换指令来完成。窄化类型转换可能会导致转换结果产生不同的正负号、不同的数量级的情况, 转换过程很可能会导致数值的精度丢失。

| 操作码    | 操作数                | 操作数栈-执行前 | 操作数栈-执行后 | 操作                                                        |
| --------- | --------------------- | --------------- | --------------- | ----------------------------------------------------------- |
| i2l       | -                     | value           | result          | 将栈顶 int 型数值强制转换为 long 型数值并将结果压入栈顶     |
| i2f       | -                     | value           | result          | 将栈顶 int 型数值强制转换为 float 型数值并将结果压入栈顶    |
| i2d       | -                     | value           | result          | 将栈顶 int 型数值强制转换为 double 型数值并将结果压入栈顶   |
| l2i       | -                     | value           | result          | 将栈顶 long 型数值强制转换为 int 型数值并将结果压入栈顶     |
| l2f       | -                     | value           | result          | 将栈顶 long 型数值强制转换为 float 型数值并将结果压入栈顶   |
| l2d       | -                     | value           | result          | 将栈顶 long 型数值强制转换为 double 型数值并将结果压入栈顶  |
| f2i       | -                     | value           | result          | 将栈顶 float 型数值强制转换为 int 型数值并将结果压入栈顶    |
| f2l       | -                     | value           | result          | 将栈顶 float 型数值强制转换为 long 型数值并将结果压入栈顶   |
| f2d       | -                     | value           | result          | 将栈顶 float 型数值强制转换为 double 型数值并将结果压入栈顶 |
| d2i       | -                     | value           | result          | 将栈顶 double 型数值强制转换为 int 型数值并将结果压入栈顶   |
| d2l       | -                     | value           | result          | 将栈顶 double 型数值强制转换为 long 型数值并将结果压入栈顶  |
| d2f       | -                     | value           | result          | 将栈顶 double 型数值强制转换为 float 型数值并将结果压入栈顶 |
| i2b       | -                     | value           | result          | 将栈顶 int 型数值强制转换为 byte 型数值并将结果压入栈顶     |
| i2c       | -                     | value           | result          | 将栈顶 int 型数值强制转换为 char 型数值并将结果压入栈顶     |
| i2s       | -                     | value           | result          | 将栈顶 int 型数值强制转换为 short 型数值并将结果压入栈顶    |
| checkcast | indexbyte1,indexbyte2 | objectref       | objectref       | 检验类型转换, 检验未通过将抛出 ClassCastException           |

说明:

- i2l: value 必须是在操作数栈栈顶的 int 类型数据, 指令执行时, 它将从操作数栈中出栈, 并带符号扩展成 long 类型数据, 然后压入到操作数栈之中
- checkcast: objectref 必须为 reference 类型的数据, indexbyte1 和 indexbyte2 用于构建一个当前类的运行时常量池的索引值, 构建方式为`(indexbyte1 << 8) | indexbyte2`, 该索引所指向的运行时常量池项应当是一个类、接口或者数组类型的符号引用。 如果 objectref 为 null 的话, 那操作数栈不会有任何变化。否则, 参数指定的类、接口或者数组类型会被虚拟机解析。如果 objectref 可以转换为这个类、接口或者数组类型, 那操作数栈就保持不变, 否则 checkcast 指令将抛出一个 ClassCastException 异常
