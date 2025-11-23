# --source 参数

在 Java 中，`--source`（或 `-source`）是 javac 编译器（以及 Java 11+ 的 java 命令）的核心选项，用于指定 Java 源代码的兼容版本（即源代码遵循的 Java 语言规范版本）。

核心作用

- 语法检查约束：编译器会按照指定的 Java 版本语法规则校验代码，禁止使用该版本之后才引入的语法特性（例如 Java 8 之后的 var 局部变量、Java 11 之后的文本块等）
- 兼容旧版本规范：确保源代码可在低版本 Java 环境中编译（或运行），避免因使用高版本语法导致的兼容性问题

## 通过 javac 使用 --source 参数

例如用 JDK 17 编译 Java 8 语法的代码（禁止使用 var、文本块等 Java 9+ 特性）：

```sh
# 若 Hello.java 中用了 var，会编译报错
javac --source 8 Hello.java
```

## 通过 java 使用 --source 参数

Java 11 起，java 命令支持直接运行未编译的 .java 文件，此时 `--source` 用于指定源代码的 Java 版本：

```sh
# 直接运行 Java 8 语法的 Hello.java
java --source 8 Hello.java
```
