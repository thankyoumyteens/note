# 字节码指令

Java 虚拟机的指令由操作码(Opcode)和操作数(Operand)构成。操作码是一个代表着特定操作的数字。操作数是操作码所需的参数。

Java 虚拟机限制了操作码的长度为一个字节，这意味着指令集的操作码总数不能够超过 256 条。

不考虑异常处理时，Java 虚拟机的解释器的执行流程为：

```java
do {
    自动计算PC寄存器的值加1;
    根据PC寄存器指示的位置，从字节码流中取出操作码;
    if (字节码存在操作数) {
        从字节码流中取出操作数;
    }
    执行操作码所定义的操作;
} while (字节码流长度 > 0);
```

在 Java 虚拟机的指令集中，大多数指令都包含其操作所对应的数据类型信息。如 iload 指令用于从局部变量表中加载 int 型的数据到操作数栈中，而 fload 指令加载的则是 float 类型的数据。这两条指令在虚拟机内部可能是由同一段代码来实现的，但在 Class 文件中它们拥有各自独立的操作码。

对于大部分与数据类型相关的字节码指令，它们的操作码助记符中都有特殊的字符来表明专门为哪种数据类型服务：i 代表对 int 类型的数据操作，l 代表 long，s 代表 short，b 代表 byte，c 代表 char，f 代表 float，d 代表 double，a 代表 reference。

编译器会在编译期或运行期将 byte 和 short 类型的数据带符号扩展为相应的 int 类型数据，将 boolean 和 char 类型数据零位扩展为相应的 int 类型数据。在处理 boolean、byte、short 和 char 类型的数组时，也会转换为使用对应的 int 类型的字节码指令来处理。因此，大多数对于 boolean、byte、short 和 char 类型数据的操作，实际上都是使用相应的对 int 类型作为运算类型来进行的。
