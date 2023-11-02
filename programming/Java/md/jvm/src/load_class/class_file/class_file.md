# 类文件结构

Class 文件格式采用一种类似于 C 语言结构体的伪结构来存储数据，这种伪结构中只有两种数据类型：无符号数和表。

- 无符号数属于基本的数据类型，以 u1、u2、u4、u8 来分别代表 1 个字节、2 个字节、4 个字节和 8 个字节的无符号数，无符号数可以用来描述数字、索引引用、数量值或者按照 UTF-8 编码构成字符串值
- 表是由多个无符号数或者其他表作为数据项构成的复合数据类型，为了便于区分，所有表的命名都习惯性地以\_info 结尾。表用于描述有层次关系的复合结构的数据，整个 Class 文件本质上也可以视作是一张表

## Class 文件结构

| 类型           | 名称                | 说明         | 长度     |
| -------------- | ------------------- | ------------ | -------- |
| u4             | magic               | 魔数         | 4 个字节 |
| u2             | minor_version       | 副版本号     | 2 个字节 |
| u2             | major_version       | 主版本号     | 2 个字节 |
| u2             | constant_pool_count | 常量池容量   | 2 个字节 |
| cp_info        | constant_pool       | 常量池       | n 个字节 |
| u2             | access_flags        | 访问标志     | 2 个字节 |
| u2             | this_class          | 类索引       | 2 个字节 |
| u2             | super_class         | 父类索引     | 2 个字节 |
| u2             | interfaces_count    | 接口个数     | 2 个字节 |
| u2             | interfaces          | 接口索引集合 | n 个字节 |
| u2             | fields_count        | 字段个数     | 2 个字节 |
| field_info     | fields              | 字段集合     | n 个字节 |
| u2             | methods_count       | 方法个数     | 2 个字节 |
| method_info    | methods             | 方法集合     | n 个字节 |
| u2             | attributes_count    | 附加属性个数 | 2 个字节 |
| attribute_info | attributes          | 附加属性集合 | n 个字节 |

## 魔数和版本号

```java
public class ClassFileDemo {
    int num;

    public int getNum() {
        return this.num;
    }
}
```

上面的代码编译成字节码后，字节码文件的内容:

![](../../img/class_file1.png)

每个 Class 文件的头 4 个字节被称为魔数(Magic Number)，它的唯一作用是确定这个文件是否为一个能被虚拟机接受的 Class 文件，固定为`0xCAFEBABE`。

紧接着魔数的 4 个字节是 Class 文件的版本号：第 5 和第 6 个字节是副版本号(Minor Version)，第 7 和第 8 个字节是主版本号(Major Version)。

Java 的版本号是从 45 开始的，JDK 1.1 之后的每个 JDK 大版本发布主版本号向上加 1，高版本的 JDK 能向下兼容以前版本的 Class 文件，但不能运行以后版本的 Class 文件。

示例中的版本号`0x0000`和`0x0037`转换成十进制是 55.0，即 JDK 11。
