# 平台模块

平台模块是 JDK 自带的模块, 提供了包括 XML 解析器、GUI 工具包等功能。

可以使用 java --list-modules 列出 JDK 所有的模块:

```sh
$ java --list-modules
java.base@21.0.2
java.compiler@21.0.2
...
jdk.accessibility@21.0.2
jdk.attach@21.0.2
...
```

以 `java.` 为前缀的平台模式是 Java SE 规范的一部分。它们通过 Java SE 的 JCP (Java Community Process)导出标准化的 API。JavaFX API 分布在共享 `javafx.` 前缀的模块中。以 `jdk.` 开头的模块包含了 JDK 特定的代码，在不同的 JDK 实现中可能会有所不同。

如果要查看某个模块的 module-info.class 文件的内容, 可以使用 `java --describe-module 模块名` 命令:

```sh
$ java --describe-module jdk.net
jdk.net@21.0.2
exports jdk.net
exports jdk.nio
requires java.base mandated
```
