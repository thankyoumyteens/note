# Unicode

Unicode 只是一个符号集, 它只规定了符号的二进制代码, 却没有规定这个二进制代码应该如何存储。

比如, 汉字"严"的 Unicode 是十六进制数4E25, 转换成二进制数足足有15位(100111000100101), 也就是说, 这个符号的表示至少需要2个字节。表示其他更大的符号, 可能需要3个字节或者4个字节, 甚至更多。

如何才能区别 Unicode 和 ASCII ？计算机怎么知道三个字节表示一个符号, 而不是分别表示三个符号呢？
所以, 为了避免混淆, 必须加入一种编码机制, 比如目前非常常用的 UTF-8 编码方式。

# UTF-8

UTF-8 是一种 Unicode 的实现方式。
其他实现方式还包括 UTF-16(字符用两个字节或四个字节表示)和 UTF-32(字符用四个字节表示)。

UTF-8 最大的一个特点, 就是它是一种变长的编码方式。它可以使用1到4个字节表示一个符号, 根据不同的符号而变化字节长度。

UTF-8 的编码规则很简单, 只有二条：
1. 对于单字节的符号, 字节的第一位设为0, 后面7位为这个符号的 Unicode 码。因此对于英语字母, UTF-8 编码和 ASCII 码是相同的。
2. 对于n字节的符号(n > 1), 第一个字节的前n位都设为1, 第n + 1位设为0, 后面字节的前两位一律设为10。剩下的没有提及的二进制位, 全部为这个符号的 Unicode 码。

# UTF-8的编码规则

字母x表示可用于编码的位。

Unicode符号范围|UTF-8编码方式
-|-
0x0000 0000 - 0x0000 007F|0xxxxxxx
0x0000 0080 - 0x0000 07FF|110xxxxx 10xxxxxx
0x0000 0800 - 0x0000 FFFF|1110xxxx 10xxxxxx 10xxxxxx
0x0001 0000 - 0x0010 FFFF|11110xxx 10xxxxxx 10xxxxxx 10xxxxxx

跟据上表, 解读 UTF-8 编码非常简单: 如果一个字节的第一位是0, 则这个字节单独就是一个字符。如果第一位是1, 则连续有多少个1, 就表示当前字符占用多少个字节。

注意：如上表所示, 每组编码靠左边的是高字节, 靠右边的是低字节。

"严"的 Unicode 是4E25(100111000100101), 根据上表, 可以发现4E25处在第三行的范围内(0x0000 0800 - 0x0000 FFFF), 因此严的 UTF-8 编码需要三个字节, 即格式是1110xxxx 10xxxxxx 10xxxxxx。然后, 从严的最后一个二进制位开始, 依次从后向前填入格式中的x, 多出的位补0。这样就得到了, 严的 UTF-8 编码是11100100 10111000 10100101, 转换成十六进制就是E4B8A5。
