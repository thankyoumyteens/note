# JVM启动参数

JVM启动参数是在运行Java程序时，用于配置JVM的一组参数。这些参数可以控制JVM的行为和性能。

## 运行Java程序

```java
java [options] classname [args]
```

其中，options是Java虚拟机参数，classname是要运行的Java类名，args是传递给main()方法的参数。


```java
java [options] -jar filename [args]
```

其中，options是Java虚拟机参数，filename是Java程序的jar包，args是传递给main()方法的参数。

## JVM参数分类

- 以`-`开头的参数是标准参数，所有的JVM都要实现这些参数，并且向后兼容
- 以`-X`开头的是非标准参数，默认JVM实现这些参数的功能，但是并不保证所有JVM实现都满足，且不保证向后兼容
- 以`-XX:`开头的是非稳定参数, 跟具体的JVM实现有关，随时可能会在下个版本取消
    - `-XX:+-Flags`形式, `+-`是对布尔值进行开关
    - `-XX:key=value`形式, 指定某个选项的值

## 系统属性参数

在启动JVM时，可以通过使用`-Dkey=value`的形式来传递指定的系统属性参数。这些参数可以在Java程序中使用 System.getProperty() 方法来获取。

示例：

```java
// 设置用户的时区为东八区 + 设置默认的文件编码为UTF-8
java -Duser.timezone=GMT+08 -Dfile.encoding=UTF-8
```

### 查看默认的所有系统属性

```java
java -XshowSettings:properties -version
```

### 查看 VM 设置

```java
java -XshowSettings:vm -version
```

## Java Agent

Java 代理(agent)是在main方法前的一个拦截器，也就是在main方法执行之前，执行agent的代码。

使用方法：

```java
// 启用外部的agent库
-javaagent:jarpath[=options] 
```

## JVM 运行模式

JVM（有两种运行模式，客户端模式（Client Mode）和服务器模式（Server Mode）。

### 客户端模式（Client Mode）：

- 客户端模式主要用于开发和调试阶段，以及对于具有较小规模的应用程序。
- 在客户端模式下，JVM会更快地启动，但可能会牺牲一些性能。
- 客户端模式适用于交互式应用程序，如桌面应用程序或开发环境。

### 服务器模式（Server Mode）：

- 服务器模式主要用于生产环境中的大型应用程序，以获得最佳的性能和吞吐量。
- 在服务器模式下，JVM会进行更多的优化，以提高应用程序的性能。
- 服务器模式适用于长时间运行的应用程序，如Web应用程序或企业级应用程序。

### 指定JVM的运行模式

- 客户端模式：-client
- 服务器模式：-server

示例：

```java
java -client Demo.class
```

## 配置JVM对字节码的处理模式

1. 解释模式（Interpretation Mode）：在解释模式下，JVM会逐行解释字节码并执行对应的操作。这种模式下的执行速度较慢，但启动速度较快，适用于调试和开发阶段
2. 即时编译模式（Just-In-Time Compilation Mode，JIT）：在即时编译模式下，JVM会将字节码实时编译成本地机器码，以提高执行速度。JIT编译器会根据代码的热点进行优化，将频繁执行的代码编译成高效的机器码。这种模式下的执行速度较快，但启动速度较慢，适用于生产环境中的大型应用程序

要配置JVM的字节码处理模式，可以使用以下参数：

- -Xint：指定解释模式
- -Xcomp：指定纯编译模式，将所有代码都编译成机器码
- -Xmixed：默认模式，混合使用解释模式和即时编译模式

## 设置JVM的堆内存

- -Xmx：设置最大堆内存。如 -Xmx4g 表示Java堆的最大值为4GB
- -Xms：设置堆内存空间的初始大小。如 -Xms512m 表示将初始堆大小设置为512MB
- -Xmn：等价于 -XX:NewSize，设置新生代的大小。如 -Xmn256m 表示将新生代的大小设置为256MB。-Xmn25% 表示将新生代的大小设置为堆内存的25%
- -XX:MaxPermSize：设置永久代的最大大小。在JDK 8及以后的版本中，此参数无效。如 -XX:MaxPermSize=256m 表示将永久代的最大大小设置为256MB
- -XX:MaxMetaspaceSize：设置元空间的最大大小。如 -XX:MaxMetaspaceSize=256m 表示将元空间的最大大小设置为256MB
- -XX:MaxDirectMemorySize，系统可以使用的最大堆外内存。如 -XX:MaxDirectMemorySize=256m 表示将直接内存的最大大小设置为256MB
- -Xss, 设置每个线程的Java栈的大小。如 -Xss1m 表示将每个线程的栈大小设置为1MB

示例：

```java
java -Xms512m -Xmx1024m Demo.class
```

## 配置垃圾回收日志

- -XX:+PrintGC：打印GC日志
- -verbose:gc：和其他GC参数组合使用，输出详细的GC信息。包括每次 GC 前后各个内存池的大小，堆内存的大小，提升到老年代的大小，以及消耗的时间
- -Xloggc:文件路径：指定将GC日志输出到指定的文件中。如 -Xloggc:/path/to/gc.log 表示将GC日志输出到gc.log中
- -XX:+PrintGCDetails：提供比 -verbose:gc 更详细的GC日志打印
- -XX:+PrintGCDateStamps：在GC日志中打印日期时间戳
- -XX:+PrintHeapAtGC：在每次GC之后打印堆的详细信息
- -XX:+PrintTenuringDistribution：打印对象在新生代中的年龄分布
- -XX:+-HeapDumpOnOutOfMemoryError：在发生OutOfMemoryError错误时生成堆转储文件，以便进行后续的分析和调试
- -XX:HeapDumpPath：与HeapDumpOnOutOfMemoryError搭配使用, 指定转储文件的目录
- -XX:OnOutOfMemoryError：在发生OutOfMemoryError错误时执行指定的命令或脚本
- -XX:OnError：在发生致命错误时执行指定的命令或脚本。如 -XX:OnError="java -version" 表示在发生致命错误时执行java -version命令
- -XX:ErrorFile=filename：指定生成的错误日志文件的保存路径

## 设置垃圾收集器

- -XX:+UseG1GC：使用G1垃圾回收器
- -XX:+UseConcMarkSweepGC：使用CMS垃圾回收器
- -XX:+UseSerialGC：使用串行垃圾回收器
- -XX:+UseParallelGC：使用并行垃圾回收器
