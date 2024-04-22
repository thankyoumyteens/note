# MANIFEST.MF 文件

MANIFEST.MF 文件是 Java JAR 文件中的一个特殊文件，它位于 JAR 文件的 META-INF 目录下。MANIFEST.MF 文件是一个文本文件，包含了 JAR 文件的配置和元数据信息，这些信息对于 Java 应用程序的运行和类加载器的类加载过程非常重要。
下面是一个简单的`MANIFEST.MF`文件示例，它包含了一些常见的属性：

```sh
Manifest-Version: 1.0
Created-By: Apache Maven 3.6.3 (https://maven.apache.org/)
Build-Jdk: 1.8.0_231-b11

Main-Class: com.example.myapp.MainApplication

Class-Path: lib/commons-lang3-3.9.jar lib/log4j-api-2.13.3.jar

Signature-Version: 1.0
Digest-Algorithms: SHA-256 SHA-512
Sealed: true

Name: /com/example/myapp/MyClass.class
SHA-256-Digest: FfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFfFf

Name: /com/example/myapp/config.properties
SHA-256-Digest: 6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z6Z

Implementation-Title: MyApp
Implementation-Version: 1.0.0
Implementation-Vendor: Example Corp.
```

这个`MANIFEST.MF`文件包含了以下属性：

1. `Manifest-Version`: 声明了清单文件的版本
2. `Created-By`: 表示创建 JAR 文件的 Java 开发工具和版本
3. `Build-Jdk`: 构建 JAR 文件时使用的 JDK 版本
4. `Main-Class`: 指定了 JAR 文件的主类，这是 Java 应用程序的入口类，这样就可以直接用 java -jar xxx.jar 来运行程序
5. `Class-Path`: 指定了 JAR 文件运行时需要的其他 JAR 文件或类路径, 类加载器会依据这个路径来搜索 class
6. `Signature-Version`: 表示签名的版本
7. `Digest-Algorithms`: 列出了用于验证 JAR 文件中条目的摘要算法
8. `Sealed`: 指示该 JAR 文件是否被密封，密封的 JAR 文件不允许添加新条目
9. `Name` 和 `SHA-256-Digest`: 为 JAR 内的特定条目提供完整性校验，`Name`属性指定了 JAR 内文件的路径，`SHA-256-Digest`是该文件的 SHA-256 哈希值
