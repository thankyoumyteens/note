# 基本数据类型

| 类型        | 说明                   | 最小长度      |
| ----------- | ---------------------- | ------------- |
| void        | 空类型, 不对应具体的值 | -             |
| bool        | 布尔类型               | -             |
| char        | 字符                   | 8 位          |
| wchar_t     | 宽字符                 | 16 位         |
| char16_t    | Unicode 字符           | 16 位         |
| char32_t    | Unicode 字符           | 32 位         |
| short       | 短整型                 | 16 位         |
| int         | 整型                   | 16 位         |
| long        | 长整型                 | 32 位         |
| long long   | 长整型                 | 64 位         |
| float       | 单精度浮点数           | 6 位有效数字  |
| double      | 双精度浮点数           | 10 位有效数字 |
| long double | 扩展精度浮点数         | 10 位有效数字 |

一个 char 的大小和一个机器字节一样。其他字符类型用于扩展字符集，如 wchar_t、char16_t、char32_t。

wchar_t 类型用于确保可以存放机器最大扩展字符集中的任意一个字符，类型 charl6_t 和 char32_t 则为 Unicode 字符集服务。

C++语言规定一个 int 至少和一个 short 一样大，一个 long 至少和一个 int 一样大，一个 long long 至少和一个 long 一样大。其中，数据类型 long long 是在 C++11 中新定义的。

## 符号

除去布尔型和扩展的字符型之外，其他整型可以划分为带符号的(signed)和无符号的(unsigned)两种。带符号类型可以表示正数、负数或 0，无符号类型则仅能表示大于等于 0 的值。

int、short、long 和 long long 都是带符号的，通过在这些类型名前添加 unsigned 就可以得到无符号类型，例如 unsigned long。类型 unsigned int 可以缩写为 unsigned。
