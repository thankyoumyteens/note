# 原始类型

JVM 支持的原始类型包括: 数值类型, `boolean` 类型, 和 `returnAddress` 类型。

数值类型由整数和浮点数组成。

整数类型包括:

- `byte`, 值是 8 位有符号的, 使用二进制补码(two's-complement)的整数, 默认值是 0
- `short`, 值是 16 位有符号的, 使用二进制补码的整数, 默认值是 0
- `int`, 值是 32 位有符号的, 使用二进制补码的整数, 默认值是 0
- `long`, 值是 64 位有符号的, 使用二进制补码的整数, 默认值是 0
- `char`, 值是 16 位无符号的整数, 在基本多文种平面(Basic Multilingual Plane)中表示 Unicode 代码点[^1], 使用 UTF-16 编码, 默认值是 '\u0000'

浮点数类型包括:

- `float`, 严格遵照 IEEE 754 标准的 binary32 格式(单精度浮点数), 默认值是+0
- `double`, 严格遵照 IEEE 754 标准的 binary64 格式(双精度浮点数), 默认值是+0

`boolean` 类型的值编码了真(true)和假(false), 默认值是 false。

`returnAddress` 类型的值是指向 JVM 字节码中操作码的指针。在原始类型中, 只有 `returnAddress` 类型不关联 Java 中的类型。

## 整数类型

整数类型的取值范围:

- `byte`, 从 -128 到 127 (-2<sup>7</sup> 到 2<sup>7</sup> - 1), 闭区间
- `short`, 从 -32768 到 32767 (-2<sup>15</sup> 到 2<sup>15</sup> - 1), 闭区间
- `int`, 从 -2147483648 到 2147483647 (-2<sup>31</sup> 到 2<sup>31</sup> - 1), 闭区间
- `long`, 从 -9223372036854775808 到 9223372036854775807 (-2<sup>63</sup> 到 2<sup>63</sup> - 1), 闭区间
- `char`, 从 0 到 65535, 闭区间

## 浮点数类型

浮点数类型包括 `float` 和 `double`, 它们的格式和操作和 IEEE 754 标准的定义相同。Java SE 15 及后续版本使用的是 2019 版本的 IEEE 754 标准, Java SE 15 之前的版本使用的是 1985 版本的 IEEE 754 标准。

IEEE 754 不仅包括正负值, 还包括正负 0, 正负无穷, 还有特别的非数字值(Not-a-Number, NaN)。
NaN 用来表示某些非法的操作, 比如零除以零。`float` 和 `double` 类型都预定义了 NaN 类型(`Float.NaN` 和 `Double.NaN`)。

有穷的非零浮点值都可以用这个公式表示: s ⋅ m ⋅ 2<sup>(e - N + 1)</sup>, 其中:

- s 是 1 或 -1, 用来控制正负
- m 是一个比 2<sup>N</sup> 小的正整数
- e 是一个在闭区间 E<sub>min</sub> = -(2<sup>K-1</sup>-2) 和 E<sub>max</sub> = 2<sup>K-1</sup>-1 之间的整数
- N 和 K 是取决于具体类型的参数

使用上面的公式, 某些值可以有多种表示形式。例如, 设一个浮点值 v 通过使用 s, m, 和 e 中的某些值可以使用上述公式表示, 如果 m 是偶数, 且 e 比 2<sup>K-1</sup>小, 可以将 m 减半, 并把 e 加 1, 就可以生成和 v 值相同的第二种表示形式。

如果 m ≥ 2<sup>N-1</sup>, 则这种表示法称为标准表示法(normalized), 否则称为次标准表示法(subnormal)。如果一个浮点值不能被 m ≥ 2<sup>N-1</sup> 的表示法表示, 那么这个值被称为次标准值(subnormal value), 因为它的值小于最小的标准值。

`float` 和 `double` 的参数 N 和 K 的约束 (以及衍生参数 E<sub>min</sub> 和 E<sub>max</sub>) 总结如下:

| 参数            | float | double |
| --------------- | ----- | ------ |
| N               | 24    | 53     |
| K               | 8     | 11     |
| E<sub>max</sub> | +127  | +1023  |
| E<sub>min</sub> | -126  | -1022  |

除了 NaN, 浮点值都是有序的。从小到大排序: 负无穷, 非零有穷负数, 正负零, 非零有穷正数, 正无穷。

IEEE 754 允许为每一个 binary32 和 binary64 的浮点格式提供许多不同的 NaN 值。然而, Java SE 平台已办会把不同浮点类型的 NaN 值统一成一个单个的典型值, 因此本规范也会把任意的 NaN 都当作典型值。

在 IEEE 754 中, 一个带有非 NaN 参数的浮点操作可能生成一个 NaN 的结果。IEEE 754 规定了一组 NaN 位模式(bit patterns)[^2], 但是并没有要求使用哪一个特定的 NaN 位模式用来表示结果; 而是留给了具体的硬件架构去决定。程序开发人员可以通过不同的位模式创建许多 NaN, 例如, 回顾性诊断信息(retrospective diagnostic information)。可以使用 `Float.intBitsToFloat` 和 `Double.longBitsToDouble` 方法分别为 `float` 和 `double` 创建 NaN。 反过来, 要检查 NaN 值的位模式, 可以分别使用 `Float.floatToRawIntBits` 和 `Double.doubleToRawLongBits` 方法。

正零和负零的值相等, 但是可以通过不同的操作来区分它们; 例如, 1.0 除以 0.0 的结果是正无穷, 而 1.0 除以 -0.0 的结果是负无穷。

NaN 是无序的, 所以比较两个 NaN 是否相等的结果为 false。如果一个变量的值是 NaN, 那么它和自己比较是否相等的结果也是 false。

## returnAddress 类型

`returnAddress` 类型是给 _`jsr`_, _`ret`_, 和 _`jsr_w`_ 指令使用的。`returnAddress` 类型的值是指向操作码的指针。与数值类型不同, `returnAddress` 类型不对应任何 Java 中的类型, 并且不会在程序运行期间被修改。

## boolean 类型

Although the Java Virtual Machine defines a `boolean` type, it only provides
very limited support for it. There are no Java Virtual Machine instructions solely
dedicated to operations on `boolean` values. Instead, expressions in the Java
programming language that operate on `boolean` values are compiled to use values
of the Java Virtual Machine int data type.

The Java Virtual Machine does directly support `boolean` arrays. Its _`newarray`_
instruction enables creation of `boolean` arrays. Arrays of type
`boolean` are accessed and modified using the byte array instructions _`baload`_ and
_`bastore`_ .

In Oracle’s Java Virtual Machine implementation, `boolean` arrays in the Java
programming language are encoded as Java Virtual Machine byte arrays, using 8 bits per
`boolean` element.

The Java Virtual Machine encodes `boolean` array components using 1 to represent
true and 0 to represent false. Where Java programming language `boolean` values
are mapped by compilers to values of Java Virtual Machine type int, the compilers
must use the same encoding.

## 注释

[^1]: Basic Multilingual Plane（BMP）是 Unicode 编码的第一部分，它包含了从 `U+0000` 到 `U+FFFF` 的字符，覆盖了大多数现代语言的字符，包括拉丁字母、希腊字母、西里尔字母、希伯来字母、阿拉伯字母、汉字、日文假名、韩文字母等。Unicode 是一种用于文本表示、编码、传输和处理的国际标准，它为世界上大多数的书写系统提供了一个唯一的数字编码。Unicode 的编码空间被分为多个平面，每个平面包含 65536 个代码点（即字符位置）。BMP 是第一个平面，也是最常用的平面，因为它包含了大多数常用的字符。
[^2]: bit patterns 指的是二进制数的序列，其中的每一位（bit）可以是 0 或 1。在 IEEE 754 标准的浮点数表示中，bit patterns 特指用于表示特定浮点数值的二进制位序列。这些位序列遵循一定的格式，包括符号位、指数位和尾数位。
