# 加载和存储指令

加载和存储指令用于将数据在栈帧中的局部变量表和操作数栈之间来回传输。

## 将一个局部变量加载到操作栈

| 操作码  | 操作数 | 操作数栈-执行前 | 操作数栈-执行后 | 操作                                               |
| ------- | ------ | --------------- | --------------- | -------------------------------------------------- |
| iload   | index  | -               | value           | 从局部变量表加载一个 int 类型值到操作数栈的栈顶    |
| lload   | index  | -               | value           | 从局部变量表加载一个 long 类型值到操作数栈的栈顶   |
| fload   | index  | -               | value           | 从局部变量表加载一个 float 类型值到操作数栈的栈顶  |
| dload   | index  | -               | value           | 从局部变量表加载一个 double 类型值到操作数栈的栈顶 |
| aload   | index  | -               | value           | 从局部变量表加载一个引用类型类型值到操作数栈的栈顶 |
| iload_0 | -      | -               | value           | 操作数是 0 的 iload 操作码的简写                   |
| iload_1 | -      | -               | value           | 操作数是 1 的 iload 操作码的简写                   |
| iload_2 | -      | -               | value           | 操作数是 2 的 iload 操作码的简写                   |
| iload_3 | -      | -               | value           | 操作数是 3 的 iload 操作码的简写                   |
| lload_0 | -      | -               | value           | 操作数是 0 的 lload 操作码的简写                   |
| lload_1 | -      | -               | value           | 操作数是 1 的 lload 操作码的简写                   |
| lload_2 | -      | -               | value           | 操作数是 2 的 lload 操作码的简写                   |
| lload_3 | -      | -               | value           | 操作数是 3 的 lload 操作码的简写                   |
| fload_0 | -      | -               | value           | 操作数是 0 的 fload 操作码的简写                   |
| fload_1 | -      | -               | value           | 操作数是 1 的 fload 操作码的简写                   |
| fload_2 | -      | -               | value           | 操作数是 2 的 fload 操作码的简写                   |
| fload_3 | -      | -               | value           | 操作数是 3 的 fload 操作码的简写                   |
| dload_0 | -      | -               | value           | 操作数是 0 的 dload 操作码的简写                   |
| dload_1 | -      | -               | value           | 操作数是 1 的 dload 操作码的简写                   |
| dload_2 | -      | -               | value           | 操作数是 2 的 dload 操作码的简写                   |
| dload_3 | -      | -               | value           | 操作数是 3 的 dload 操作码的简写                   |
| aload_0 | -      | -               | value           | 操作数是 0 的 aload 操作码的简写                   |
| aload_1 | -      | -               | value           | 操作数是 1 的 aload 操作码的简写                   |
| aload_2 | -      | -               | value           | 操作数是 2 的 aload 操作码的简写                   |
| aload_3 | -      | -               | value           | 操作数是 3 的 aload 操作码的简写                   |

说明: index 是一个代表当前栈帧中局部变量表的索引的无符号 byte 类型整数, index 作为索引定位的局部变量必须是 int/long/float/double/引用 类型, 记为 value。指令执行后, value 将会压入到操作数栈的栈顶

## 将一个数值从操作数栈存储到局部变量表

包含的指令: istore, `istore_<n>`, lstore, `lstore_<n>`, fstore, `fstore_<n>`, dstore, `dstore_<n>`, astore, `astore_<n>`

| 操作码   | 操作数 | 操作数栈-执行前 | 操作数栈-执行后 | 操作                                         |
| -------- | ------ | --------------- | --------------- | -------------------------------------------- |
| istore   | index  | value           | -               | 将栈顶 int 型数值存入局部变量表中指定位置    |
| lstore   | index  | value           | -               | 将栈顶 long 型数值存入局部变量表中指定位置   |
| fstore   | index  | value           | -               | 将栈顶 float 型数值存入局部变量表中指定位置  |
| dstore   | index  | value           | -               | 将栈顶 double 型数值存入局部变量表中指定位置 |
| astore   | index  | value           | -               | 将栈顶引用类型数值存入局部变量表中指定位置   |
| istore_0 | -      | value           | -               | 操作数是 0 的 istore 操作码的简写            |
| istore_1 | -      | value           | -               | 操作数是 1 的 istore 操作码的简写            |
| istore_2 | -      | value           | -               | 操作数是 2 的 istore 操作码的简写            |
| istore_3 | -      | value           | -               | 操作数是 3 的 istore 操作码的简写            |
| lstore_0 | -      | value           | -               | 操作数是 0 的 lstore 操作码的简写            |
| lstore_1 | -      | value           | -               | 操作数是 1 的 lstore 操作码的简写            |
| lstore_2 | -      | value           | -               | 操作数是 2 的 lstore 操作码的简写            |
| lstore_3 | -      | value           | -               | 操作数是 3 的 lstore 操作码的简写            |
| fstore_0 | -      | value           | -               | 操作数是 0 的 fstore 操作码的简写            |
| fstore_1 | -      | value           | -               | 操作数是 1 的 fstore 操作码的简写            |
| fstore_2 | -      | value           | -               | 操作数是 2 的 fstore 操作码的简写            |
| fstore_3 | -      | value           | -               | 操作数是 3 的 fstore 操作码的简写            |
| dstore_0 | -      | value           | -               | 操作数是 0 的 dstore 操作码的简写            |
| dstore_1 | -      | value           | -               | 操作数是 1 的 dstore 操作码的简写            |
| dstore_2 | -      | value           | -               | 操作数是 2 的 dstore 操作码的简写            |
| dstore_3 | -      | value           | -               | 操作数是 3 的 dstore 操作码的简写            |
| astore_0 | -      | value           | -               | 操作数是 0 的 astore 操作码的简写            |
| astore_1 | -      | value           | -               | 操作数是 1 的 astore 操作码的简写            |
| astore_2 | -      | value           | -               | 操作数是 2 的 astore 操作码的简写            |
| astore_3 | -      | value           | -               | 操作数是 3 的 astore 操作码的简写            |

说明: index 是一个无符号 byte 型整数, 它是当前栈帧局部变量表的索引值, 而在操作数栈栈顶的 value 必须是 int/long/float/double/引用 类型的数据, 这个数据将从操作数栈出栈, 然后保存到 index 所指向的局部变量表位置中

## 将一个常量加载到操作数栈

| 操作码      | 操作数                | 操作数栈-执行前 | 操作数栈-执行后 | 操作                                     |
| ----------- | --------------------- | --------------- | --------------- | ---------------------------------------- |
| bipush      | byte                  | -               | value           | 将 byte 类型数据(-128~127)入栈           |
| sipush      | byte1,byte2           | -               | value           | 将 short 类型数据(-32768~32767)入栈      |
| ldc         | index                 | -               | value           | 将常量池中 int/float/String 类型数据入栈 |
| ldc_w       | indexbyte1,indexbyte2 | -               | value           | 将常量池中 int/float/String 类型数据入栈 |
| ldc2_w      | indexbyte1,indexbyte2 | -               | value           | 将常量池中 long/double 类型数据入栈      |
| aconst_null | -                     | -               | null            | 将 null 推送至栈顶                       |
| iconst_m1   | -                     | -               | -1              | 将 int 类型数据 -1 推送至栈顶            |
| iconst_0    | -                     | -               | 0               | 将 int 类型数据 0 推送至栈顶             |
| iconst_1    | -                     | -               | 1               | 将 int 类型数据 1 推送至栈顶             |
| iconst_2    | -                     | -               | 2               | 将 int 类型数据 2 推送至栈顶             |
| iconst_3    | -                     | -               | 3               | 将 int 类型数据 3 推送至栈顶             |
| iconst_4    | -                     | -               | 4               | 将 int 类型数据 4 推送至栈顶             |
| iconst_5    | -                     | -               | 5               | 将 int 类型数据 5 推送至栈顶             |
| lconst_0    | -                     | -               | 0               | 将 long 类型数据 0 推送至栈顶            |
| lconst_1    | -                     | -               | 1               | 将 long 类型数据 1 推送至栈顶            |
| fconst_0    | -                     | -               | 0               | 将 float 类型数据 0 推送至栈顶           |
| fconst_1    | -                     | -               | 1               | 将 float 类型数据 1 推送至栈顶           |
| fconst_2    | -                     | -               | 2               | 将 float 类型数据 2 推送至栈顶           |
| dconst_0    | -                     | -               | 0               | 将 double 类型数据 0 推送至栈顶          |
| dconst_1    | -                     | -               | 1               | 将 double 类型数据 1 推送至栈顶          |

说明:

- bipush: 将 byte 带符号扩展为一个 int 类型的值 value, 然后将 value 压入到操作数栈中
- sipush: 无符号数 byte1 和 byte2 通过`(byte1 << 8) | byte2` 方式构造成一个 short 类型数值, 然后此数值带符号扩展为一个 int 类型的值 value, 然后将 value 压入到操作数栈中
- ldc: index 是一个无符号 byte 型数据, 它作为当前类的运行时常量池的索引使用。index 指向的运行时常量池项必须是一个 int 或者 float 类型的运行时常量, 或者是一个类的符号引用或者字符串字面量。如果运行时常量池项是一个 int 或者 float 类型的运行时常量, 那这个常量所对应的数值 value 将被压入到操作数栈之中。如果运行时常量池项是一个代表字符串字面量的 String 类的引用, 那这个引用所对应的 reference 类型数据 value 将被压入到操作数栈之中。如果运行时常量池项是一个类的符号引用, 且这个符号引用是已被解析过的, 那这个类的 Class 对象所对应的 reference 类型数据 value 将被压入到操作数栈之中
- ldc_w: 无符号数 indexbyte1 和 indexbyte2 用于构建一个当前类的运行时常量池的索引值, 构建方式为`(indexbyte1 << 8) | indexbyte2`, 该索引所指向的运行时常量池项应当是一个 int 或者 float 类型的运行时常量, 或者是一个类的符号引用或者字符串字面量。ldc_w 指令与 ldc 指令的差别在于它使用了更宽的运行时常量池索引
- ldc2_w: 无符号数 indexbyte1 和 indexbyte2 用于构建一个当前类的运行时常量池的索引值, 构建方式为`(indexbyte1 << 8) | indexbyte2`, 该索引所指向的运行时常量池项应当是一个 long 或者 double 类型的运行时常量, 这个常量所对应的数值将被压入到操作数栈之中
