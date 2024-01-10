# 版本号

魔数后面的 4 个字节是 class 文件的版本号: 第 5 和第 6 个字节是副版本号(Minor Version), 第 7 和第 8 个字节是主版本号(Major Version)。

Java 的版本号是从 45 开始的, JDK 1.1 之后的每个 JDK 大版本发布主版本号向上加 1, 高版本的 JDK 能向下兼容以前版本的 class 文件, 但不能运行以后版本的 class 文件。

ClassFileDemo.class 文件中的版本号 0x0041.0x0000 转换成十进制是 65.0, 即 JDK 21。

![](../../img/class_file_version.png)
