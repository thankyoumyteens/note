# 应用程序类数据共享

Java 10 对应用程序类数据共享（Application Class-Data Sharing，AppCDS） 进行了重要扩展，在原有类数据共享（CDS） 的基础上，允许将应用程序类和第三方库类加入共享归档文件，进一步提升应用启动速度和减少内存占用，尤其对大型应用和容器化环境更友好。

Java 5 引入的 CDS 仅支持共享 JVM 核心类（如 `java.lang.*`、`java.util.*` 等 rt.jar 中的类），通过将这些类的元数据和静态数据预编译为归档文件（classes.jsa），实现多个 JVM 实例共享，从而减少启动时间和内存消耗。

但传统 CDS 存在明显局限：

- 仅支持 JDK 自带的核心类，应用程序自身的类和第三方库（如 Spring、Guava 等）无法共享
- 对于类数量庞大的应用（如企业级 Java 应用），启动时仍需大量时间加载和验证应用类，启动速度提升有限

Java 10 的 AppCDS 突破了传统 CDS 的限制，支持将应用程序类、第三方库类与 JVM 核心类一起纳入共享归档，实现更全面的类数据共享。

## AppCDS 的工作原理

1. 生成类列表：通过运行应用，记录所有加载的类，生成一个 “类列表文件”（包含应用类、第三方库类和核心类）
2. 创建共享归档：根据类列表，将这些类的元数据和静态数据编译为一个共享归档文件（.jsa）
3. 使用共享归档：后续启动应用时，JVM 直接从共享归档加载类数据，跳过解析、验证等步骤，加速启动

## 使用步骤

### 1. 生成类列表

首次运行应用时，通过以下参数记录所有加载的类，生成列表文件（如 app.classlist）：

```sh
java -XX:DumpLoadedClassList=app.classlist -jar myapp.jar
```

该过程会正常启动应用，退出时将所有加载的类（包括 JDK 类、应用类、第三方库类）写入 app.classlist。

根据类列表，生成包含这些类的共享归档文件（如 app.jsa）：

### 2. 创建共享归档

根据类列表，生成包含这些类的共享归档文件（如 app.jsa）：

```sh
java -Xshare:dump -XX:SharedClassListFile=app.classlist \
     -XX:SharedArchiveFile=app.jsa \
     -cp myapp.jar:lib/*  # 需指定应用的类路径（确保能找到列表中的类）
```

生成的 app.jsa 包含类列表中所有类的预编译数据。

### 3. 使用共享归档启动应用

后续启动应用时，通过以下参数加载共享归档，加速启动：

```sh
java -Xshare:on -XX:SharedArchiveFile=app.jsa -jar myapp.jar
```

JVM 会优先从 app.jsa 加载类，未包含在归档中的类仍从类路径加载。
