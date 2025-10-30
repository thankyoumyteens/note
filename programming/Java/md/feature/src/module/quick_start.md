# 使用模块

创建如下结构:

```
jpms-demo
└── src
    └── hello
        ├── com
        │   └── example
        │       └── Hello.java
        └── module-info.java
```

Hello.java 内容如下:

```java
package com.example;

public class Hello {
    public static void main(String[] args) {
        System.out.println("hello");
    }
}
```

## 模块描述符

相比于 Java 源文件的传统布局，上述布局存在两个主要区别:

1. 首先，有一个额外的间接层: 在 src 的下面引入了另一个目录 hello, 该目录以所创建的模块名称命名
2. 其次，在模块目录 hello 中包含源文件 Hello.java 和一个模块描述符

模块描述符位于 module-info.java 文件中，是 Java 模块的关键组成部分。它的存在相当于告诉 Java 编译器正在使用的是一个模块，而不是普通的 Java 源代码。

与普通的 Java 源文件相比，当使用模块时，编译器的行为是完全不同的。模块描述符必须存在于模块目录的根目录中。它与其他源文件一起编译成一个名为 module-info.class 的二进制 class 文件。

module-info.java 内容如下:

```java
module hello {
}
```

在 module-info.java 中, 使用关键字 module 声明了一个模块。模块名是 hello, 该名称必须与包含模块描述符的目录名称相匹配。否则，编译器将拒绝编译井报告匹配错误。

## 编译

```sh
javac -d out/hello \
    src/hello/com/example/Hello.java \
    src/hello/module-info.java
```

编译后的结果, 也被称为分解模块(exploded module)格式:

```
out
└── hello
    ├── com
    │   └── example
    │       └── Hello.class
    └── module-info.class
```

## 将模块打包成 JAR

模块化 JAR 文件类似于普通的 JAR 文件，但它还包含了 module-info.class。

```sh
jar -cfe mods/hello.jar \
    com.example.Hello \
    -C out/hello/ .
```

jar 命令通过 `-cf` 参数在 mods 目录中创建了一个 hello.jar 文件。此外，通过 `-e` 参数指定这个模块的入口是 com.example.Hello 类, 每当模块启动并且没有指定另一个要运行的主类时，这是默认的入口。最后，通过 `-C` 参数将 out/hello 目录中的所有已编译文件放到 jar 包中。同时还额外添加了一个 MANIFESTMF 文件:

```
hello.jar
├── META-INF
│   └── MANIFEST.MF
├── com
│   └── example
│       └── Hello.class
└── module-info.class
```

## 运行模块

通过模块化 jar 包运行:

```sh
java --module-path mods --module hello
```

或者通过分解模块格式运行:

```sh
java --module-path out \
    --module hello/com.example.Hello
```

`--module-path` 可以缩写成 `-p`。`--module`可以缩写成 `-m`。

以这两种方式中的任何一种启动都会使 hello 成为执行的根模块。JVM 从这个根模块开始，解析从模块路径运行根模块所需的任何其他模块。

## 输出解析的模块

```sh
java --show-module-resolution \
    --limit-modules java.base \
    --module-path out \
    --module hello/com.example.Hello
```

此时，除了隐式需要的平台模块 java.base 之外，不再需要其他模块来运行 hello。其他平台模块或者模块路径上的模块都没有解析。在类加载期间，没有任何资源被浪费在搜索与应用程序无关的类上。

## 链接模块

创建自定义运行时映像(custom runtime image):

```sh
jlink --module-path mods/:$JAVA_HOME/jmods \
    --add-modules hello \
    --launcher run_app=hello \
    --output hello-image
```

`--module-path` 构造一个模块路径，其中包含 mods 目录(hello 模块所在的位置)以及要链接到映像中的平台模块目录。与 javac 和 java 不同，必须将平台模块显式添加到 jlink 模块路径中。随后，`--add-modules` 表示 hello 模块是需要在运行时映像中运行的根模块。`--launcher` 定义了一个入口来直接运行映像中的模块。最后，`--output` 表示运行时映像的目录名称。

运行上述命令的结果是生成一个新目录，包含了一个完全适合运行 hello 的 Java 运行时：

```
hello-image
├── bin
│   ├── java
│   ├── keytool
│   └── run_app
├── conf
│   └── ...
├── include
│   └── ...
├── legal
│   └── ...
├── lib
│   └── ...
├── man
│   └── ...
└── release
```

bin/run_app 是一个平台相关的可执行程序, 可以直接启动:

```sh
./hello-image/bin/run_app
```
