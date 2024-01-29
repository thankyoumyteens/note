# 跳转指令

对于 boolean 类型、byte 类型、char 类型和 short 类型的条件分支比较操作, 都使用 int 类型的比较指令来完成。而对于 long 类型、float 类型和 double 类型的条件分支比较操作, 则会先执行相应类型的比较运算指令(dcmpg、dcmpl、fcmpg、fcmpl、lcmp), 运算指令会返回一个整型值到操作数栈中, 随后再执行 int 类型的条件分支比较操作来完成整个分支跳转。

## 条件分支

| 操作码    | 操作数                  | 操作数栈-执行前 | 操作数栈-执行后 | 操作                                               |
| --------- | ----------------------- | --------------- | --------------- | -------------------------------------------------- |
| ifeq      | branchbyte1,branchbyte2 | value           | -               | 当栈顶 int 型数值等于 0 时跳转                     |
| ifne      | branchbyte1,branchbyte2 | value           | -               | 当栈顶 int 型数值不等于 0 时跳转                   |
| iflt      | branchbyte1,branchbyte2 | value           | -               | 当栈顶 int 型数值小于 0 时跳转                     |
| ifge      | branchbyte1,branchbyte2 | value           | -               | 当栈顶 int 型数值大于等于 0 时跳转                 |
| ifgt      | branchbyte1,branchbyte2 | value           | -               | 当栈顶 int 型数值大于 0 时跳转                     |
| ifle      | branchbyte1,branchbyte2 | value           | -               | 当栈顶 int 型数值小于等于 0 时跳转                 |
| if_icmpeq | branchbyte1,branchbyte2 | value1,value2   | -               | 比较栈顶两 int 型数值大小, 当结果等于 0 时跳转     |
| if_icmpne | branchbyte1,branchbyte2 | value1,value2   | -               | 比较栈顶两 int 型数值大小, 当结果不等于 0 时跳转   |
| if_icmplt | branchbyte1,branchbyte2 | value1,value2   | -               | 比较栈顶两 int 型数值大小, 当结果小于 0 时跳转     |
| if_icmpge | branchbyte1,branchbyte2 | value1,value2   | -               | 比较栈顶两 int 型数值大小, 当结果大于等于 0 时跳转 |
| if_icmpgt | branchbyte1,branchbyte2 | value1,value2   | -               | 比较栈顶两 int 型数值大小, 当结果大于 0 时跳转     |
| if_icmple | branchbyte1,branchbyte2 | value1,value2   | -               | 比较栈顶两 int 型数值大小, 当结果小于等于 0 时跳转 |
| if_acmpeq | branchbyte1,branchbyte2 | value1,value2   | -               | 比较栈顶两引用型数值, 当结果相等时跳转             |
| if_acmpne | branchbyte1,branchbyte2 | value1,value2   | -               | 比较栈顶两引用型数值, 当结果不相等时跳转           |

说明:

- ifxx: value 必须为 int 类型数据, 指令执行时, value 从操作数栈中出栈, 然后与零值进行比较, 如果比较结果为真, 那无符号 byte 型数据 branchbyte1 和 branchbyte2 用于构建一个 16 位有符号的分支偏移量, 构建方式为`(branchbyte1 << 8) | branchbyte2`。指令执行后, 程序将会转到这个 ifxx 指令之后的, 由上述偏移量确定的目标地址上继续执行。这个目标地址必须处于 ifxx 指令所在的方法之中。另外, 如果比较结果为假, 那程序将继续执行 ifxx 指令下面的其他字节码指令。比较的规则如下:
  - eq: 当且仅当 value == 0 时, 比较的结果为真
  - ne: 当且仅当 value != 0 时, 比较的结果为真
  - lt: 当且仅当 value < 0 时, 比较的结果为真
  - le: 当且仅当 value <= 0 时, 比较的结果为真
  - ge: 当且仅当 value > 0 时, 比较的结果为真
  - ge: 当且仅当 value >= 0 时, 比较的结果为真
- if_icmpxx: value1 和 value2 都必须为 int 类型数据, 指令执行时, value1 和 value2 从操作数栈中出栈, 然后进行比较运算, 如果比较结果为真, 那无符号 byte 型数据 branchbyte1 和 branchbyte2 用于构建一个 16 位有符号的分支偏移量, 构建方式为`(branchbyte1 << 8) | branchbyte2`。指令执行后, 程序将会转到这个 if_icmpxx 指令之后的, 由上述偏移量确定的目标地址上继续执行。这个目标地址必须处于 if_icmpxx 指令所在的方法之中。另外, 如果比较结果为假, 那程序将继续执行 if_acmpxx 指令后面的其他字节码指令。 比较的规则如下：
  - eq 当且仅当 value1 == value2 时, 比较的结果为真
  - ne 当且仅当 value1 != value2 时, 比较的结果为真
  - lt 当且仅当 value1 < value2 时, 比较的结果为真
  - le 当且仅当 value1 <= value2 时, 比较的结果为真
  - ge 当且仅当 value1 > value2 时, 比较的结果为真
  - ge 当且仅当 value1 >= value2 时, 比较的结果为真

## tableswitch

switch 语句的 case 值连续时, 会生成 tableswitch 指令, tableswitch 的格式:

```
操作码:
        tableswitch
操作数:
        <0-3 byte pad>
        defaultbyte1
        defaultbyte2
        defaultbyte3
        defaultbyte4
        lowbyte1
        lowbyte2
        lowbyte3
        lowbyte4
        highbyte1
        highbyte2
        highbyte3
        highbyte4
        jump offsets...
操作数栈-执行前:
        index
操作数栈-执行后:
        -
```

说明:

- tableswitch: tableswitch 是一条变长指令。紧跟 tableswitch 之后的 0 至 3 个字节作为空白填充, 而后面 defaultbyte1 至 defaultbyte4 代表了一个个由 4 个字节组成的、从当前方法开始（第一条操作码指令）计算的地址, 即紧跟随空白填充的是一系列 32 位有符号整数值：包括默认跳转地址 default、高位值 high 以及低位值 low。在此之后, 是 high-low+1 个有符号 32 位偏移量 offset, 其中要求 low 小于或等于 high。这 high-low+1 个 32 位有符号数值形成一张零基址跳转表, 所有上述的 32 位有符号数都以`(byte1 << 24) | (byte2 << 16) | (byte3 << 8) | byte4`方式构成。指令执行时, int 型的 index 从操作数栈中出栈, 如果 index 比 low 值小或者比 high 值大, 那就是用 default 作为目标地址进行跳转。否则, 在跳转表中第 index-low 个地址值将作为目标地址进行跳转, 程序从目标地址开始继续执行。目标地址既可能从跳转表匹配坐标中得出, 也可能从 default 中得出, 但无论如何, 最终的目标地址必须在包含 tableswitch 指令的那个方法之内

示例代码:

```java
int r = new Random().nextInt();
switch (r) {
    case 10:
        System.out.println("0");
        break;
    case 11:
        System.out.println("1");
        break;
    case 12:
        System.out.println("2");
        break;
    default:
        System.out.println("-1");
        break;
}
```

编译后, 查看字节码, 找到 tableswitch 指令, 整理后如下:

```java
AA                   // tableswitch
00 00 00             // 3字节填充
00 00 00 3D          // defaultbyte1~defaultbyte4, 十进制61
00 00 00 0A          // lowbyte1~lowbyte4, 十进制10
00 00 00 0C          // highbyte1~highbyte4, 十进制12
// high-low+1=3个offset
00 00 00 1C          // offset0, 十进制28
00 00 00 27          // offset1, 十进制39
00 00 00 32          // offset2, 十进制50
```

使用 javap 查看:

```java
 0: new           #2    // class java/util/Random
 3: dup
 4: invokespecial #3    // Method java/util/Random."<init>":()V
 7: invokevirtual #4    // Method java/util/Random.nextInt:()I
10: istore_1
11: iload_1
12: tableswitch   {     // case 10 到 case 12
            10: 40      // offset0, 28+12=40
            11: 51      // offset1, 39+12=51
            12: 62      // offset2, 50+12=62
        default: 73     // defaultbyte1~defaultbyte4, 61+12=73
    }
40: getstatic     #5    // Field java/lang/System.out:Ljava/io/PrintStream;
43: ldc           #6    // String 0
45: invokevirtual #7    // Method java/io/PrintStream.println:(Ljava/lang/String;)V
48: goto          81
51: getstatic     #5    // Field java/lang/System.out:Ljava/io/PrintStream;
54: ldc           #8    // String 1
56: invokevirtual #7    // Method java/io/PrintStream.println:(Ljava/lang/String;)V
59: goto          81
62: getstatic     #5    // Field java/lang/System.out:Ljava/io/PrintStream;
65: ldc           #9    // String 2
67: invokevirtual #7    // Method java/io/PrintStream.println:(Ljava/lang/String;)V
70: goto          81
73: getstatic     #5    // Field java/lang/System.out:Ljava/io/PrintStream;
76: ldc           #10   // String -1
78: invokevirtual #7    // Method java/io/PrintStream.println:(Ljava/lang/String;)V
81: return
```

## lookupswitch

switch 语句的 case 值不连续时, 会生成 lookupswitch 指令, lookupswitch 的格式:

```
操作码:
        lookupswitch
操作数:
        <0-3 byte pad>
        defaultbyte1
        defaultbyte2
        defaultbyte3
        defaultbyte4
        npairs1
        npairs2
        npairs3
        npairs4
        match-offset pairs...
操作数栈-执行前:
        key
操作数栈-执行后:
        -
```

说明:

- lookupswitch: lookupswitch 是一条变长指令。紧跟 lookupswitch 之后的 0 至 3 个字节作为空白填充, 而后面 defaultbyte1 至 defaultbyte4 等代表了一个个由 4 个字节组成的、从当前方法开始（第一条操作码指令）计算的地址, 即紧跟随空白填充的是一系列 32 位有符号整数值：包括默认跳转地址 default、匹配坐标的数量 npairs 以及 npairs 组匹配坐标。其中, npairs 的值应当大于或等于 0, 每一组匹配坐标都包含了一个整数值 match 以及一个有符号 32 位偏移量 offset。上述所有的 32 位有符号数值都以`(byte1 << 24) | (byte2 << 16) | (byte3 << 8) | byte4`方式构成。lookupswitch 指令之后所有的匹配坐标必须以其中的 match 值排序, 按照升序储存。指令执行时, int 型的 key 从操作数栈中出栈, 与每一个 match 值相互比较。如果能找到一个与之相等的 match 值, 那就就以这个 match 所配对的偏移量 offset 作为目标地址进行跳转。如果没有配对到任何一个 match 值, 那就是用 default 作为目标地址进行跳转。程序从目标地址开始继续执行。目标地址既可能从 npairs 组匹配坐标中得出, 也可能从 default 中得出, 但无论如何, 最终的目标地址必须在包含 lookupswitch 指令的那个方法之内

示例代码:

```java
int r = new Random().nextInt();
switch (r) {
    case 0:
        System.out.println("0");
        break;
    case 10:
        System.out.println("1");
        break;
    case 20:
        System.out.println("2");
        break;
    default:
        System.out.println("-1");
        break;
}
```

编译后, 查看字节码, 找到 lookupswitch 指令, 整理后如下:

```java
AB                   // lookupswitch
00 00 00             // 3字节填充
00 00 00 45          // defaultbyte1~defaultbyte4, 十进制69
00 00 00 03          // npairs1~npairs4, 十进制3
// 3个match-offset pairs
00 00 00 00          // pair0-match, 十进制0
00 00 00 24          // pair0-offset, 十进制36
00 00 00 0A          // pair1-match, 十进制10
00 00 00 2F          // pair1-offset, 十进制47
00 00 00 14          // pair2-match, 十进制20
00 00 00 3A          // pair2-offset, 十进制58
```

使用 javap 查看:

```java
 0: new           #2    // class java/util/Random
 3: dup
 4: invokespecial #3    // Method java/util/Random."<init>":()V
 7: invokevirtual #4    // Method java/util/Random.nextInt:()I
10: istore_1
11: iload_1
12: lookupswitch  {     // 3
            0: 48       // pair0, match: 0, offset: 36+12=48
            10: 59      // pair1, match: 10, offset: 47+12=59
            20: 70      // pair2, match: 20, offset: 58+12=70
        default: 81     // defaultbyte1~defaultbyte4, 69+12=81
}
48: getstatic     #5    // Field java/lang/System.out:Ljava/io/PrintStream;
51: ldc           #6    // String 0
53: invokevirtual #7    // Method java/io/PrintStream.println:(Ljava/lang/String;)V
56: goto          89
59: getstatic     #5    // Field java/lang/System.out:Ljava/io/PrintStream;
62: ldc           #8    // String 1
64: invokevirtual #7    // Method java/io/PrintStream.println:(Ljava/lang/String;)V
67: goto          89
70: getstatic     #5    // Field java/lang/System.out:Ljava/io/PrintStream;
73: ldc           #9    // String 2
75: invokevirtual #7    // Method java/io/PrintStream.println:(Ljava/lang/String;)V
78: goto          89
81: getstatic     #5    // Field java/lang/System.out:Ljava/io/PrintStream;
84: ldc           #10   // String -1
86: invokevirtual #7    // Method java/io/PrintStream.println:(Ljava/lang/String;)V
89: return
```

## 无条件分支

| 操作码 | 操作数                                          | 操作数栈-执行前 | 操作数栈-执行后 | 操作                                                                |
| ------ | ----------------------------------------------- | --------------- | --------------- | ------------------------------------------------------------------- |
| goto   | branchbyte1,branchbyte2                         | -               | -               | 无条件跳转                                                          |
| goto_w | branchbyte1,branchbyte2,branchbyte3,branchbyte4 | -               | -               | 无条件跳转                                                          |
| jsr    | branchbyte1,branchbyte2                         | -               | address         | 跳转至指定的 16 位 offset 位置, 并将 jsr 的下一条指令地址压入栈顶   |
| jsr_w  | branchbyte1,branchbyte2,branchbyte3,branchbyte4 | -               | address         | 跳转至指定的 32 位 offset 位置, 并将 jsr_w 的下一条指令地址压入栈顶 |
| ret    | index                                           | -               | -               | 返回至本地变量指定的 index 的指令位置(一般与 jsr 或 jsr_w 联合使用) |

说明:

- goto: 无符号 byte 型数据 branchbyte1 和 branchbyte2 用于构建一个 16 位有符号的分支偏移量, 构建方式为`(branchbyte1 << 8) | branchbyte2`。指令执行后, 程序将会转到这个 goto 指令之后的, 由上述偏移量确定的目标地址上继续执行。这个目标地址必须处于 goto 指令所在的方法之中
- goto_w: 无符号 byte 型数据 branchbyte1、branchbyte2、branchbyte3 和 branchbyte4 用于构建一个 32 位有符号的分支偏移量, 构建方式为`(branchbyte1 << 24) | (branchbyte2 << 16) | (branchbyte3 << 8) | branchbyte4`。指令执行后, 程序将会转到这个 goto_w 指令之后的, 由上述偏移量确定的目标地址上继续执行。这个目标地址必须处于 goto_w 指令所在的方法之中
- jsr: address 是一个 returnAddress 类型的数据, 它由 jsr 指令推入操作数栈中。无符号 byte 型数据 branchbyte1 和 branchbyte2 用于构建一个 16 位有符号的分支偏移量, 构建方式为`(branchbyte1 << 8) | branchbyte2`。指令执行时, 将产生一个当前位置的偏移坐标, 并压入到操作数栈中。跳转目标地址必须在 jsr 指令所在的方法之内
- jsr_w: address 是一个 returnAddress 类型的数据, 它由 jsr_w 指令推入操作数栈中。无符号 byte 型数据 branchbyte1、branchbyte2、branchbyte3 和 branchbyte4 用于构建一个 32 位有符号的分支偏移量, 构建方式为`(branchbyte1 << 24) | (branchbyte2 << 16) | (branchbyte3 << 8) | branchbyte4`。指令执行时, 将产生一个当前位置的偏移坐标, 并压入到操作数栈中。跳转目标地址必须在 jsr_w 指令所在的方法之内
- ret: index 是一个 0 至 255 之间的无符号数, 它代表一个当前栈帧的局部变量表的索引值, 在该索引位置应为一个 returnAddress 类型的局部变量, 指令执行后, 将该局部变量的值更新到 JVM 的程序计数器中, 令程序从修改后的位置继续执行。ret 指令被用来与 jsr、jsr_w 指令一同实现 Java 语言中的 finally 语句块。请注意, jsr_w 指令推送 address 到操作数栈, ret 指令从局部变量表中把它取出
