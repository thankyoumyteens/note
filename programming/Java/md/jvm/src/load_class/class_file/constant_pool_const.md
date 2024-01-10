# 常量池中的常量

常量池中主要存放两大类常量: 字面量(Literal)和符号引用(Symbolic References)。

- 字面量比较接近于 Java 的常量概念, 如文本字符串、被声明为 final 的常量值等
- 符号引用主要包括: 被模块导出或者开放的包、类和接口的全限定名、字段的名称和描述符、方法的名称和描述符、方法句柄和方法类型、动态调用点和动态常量

Java 代码在进行编译的时候, 并不像 C 和 C++那样有链接这一步骤, 而是在 JVM 进行类加载的时候进行动态连接。在 class 文件中不会保存各个方法、字段最终在内存中的地址。当 JVM 加载类时, 会从常量池中获得对应的符号引用, 再把符号引用转换成具体的内存地址。

常量池中每一项常量都是一个表, 截止到 JDK21, 常量池中有 17 种不同类型的常量。每一个常量表结构的第一位是个 u1 类型的标志位, 代表着当前常量属于哪种常量类型。这 17 种常量类型各自有着完全独立的数据结构。

| 类型                        | 标志(十进制) | 说明                       |
| --------------------------- | ------------ | -------------------------- |
| CONSTANT_Utf8               | 1            | UTF-8 编码的字符串         |
| CONSTANT_Integer            | 3            | 整型字面量                 |
| CONSTANT_Float              | 4            | 浮点型字面量               |
| CONSTANT_Long               | 5            | 长整型字面量               |
| CONSTANT_Double             | 6            | 双精度浮点型字面量         |
| CONSTANT_Class              | 7            | 类或接口的符号引用         |
| CONSTANT_String             | 8            | 字符串类型字面量           |
| CONSTANT_Fieldref           | 9            | 字段的符号引用             |
| CONSTANT_Methodref          | 10           | 类中方法的符号引用         |
| CONSTANT_InterfaceMethodref | 11           | 接口中方法的符号引用       |
| CONSTANT_NameAndType        | 12           | 字段或方法的部分符号引用   |
| CONSTANT_MethodHandle       | 15           | 方法句柄                   |
| CONSTANT_MethodType         | 16           | 方法类型                   |
| CONSTANT_Dynamic            | 17           | 动态计算常量               |
| CONSTANT_InvokeDynamic      | 18           | 动态方法调用点             |
| CONSTANT_Module             | 19           | 模块                       |
| CONSTANT_Package            | 20           | 一个模块中开放或者导出的包 |
