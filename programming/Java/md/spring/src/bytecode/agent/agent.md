# Java Agent

Java Agent 是基于 JVMTI 实现的, 它允许外部 jar 包以代理的方式挂载到目标 JVM 中, 动态修改运行中的 Java 程序。

Java Agent 主要涉及以下几个部分：

1. Instrumentation API：Java Agent 通过`java.lang.instrument`包中的`Instrumentation`接口与目标 JVM 进行交互。这个接口提供了一系列方法, 允许对 JVM 中的类进行操作, 如类定义转换、获取所有已加载的类等。`java.lang.instrument`包实际上是对 JVMTI 的一种高级封装
2. Agent 类：实现 Java Agent 的核心类需要实现`premain`方法。这个方法在目标程序的`main`方法执行之前被调用, 它接收`Instrumentation`实例作为参数, 可以在这个方法中注册 Class Transformer
3. Attach API：如果需要在 JVM 启动后动态加载 Agent, 可以使用 Attach API。使用 Attach API 时, 目标 JVM 进程需要开启一个特殊的通信端口以供外部连接
4. Class Transformer：通过`Instrumentation`接口的`addTransformer`方法, 可以注册一个`ClassFileTransformer`。当类被加载时, JVM 会调用这些转换器, 允许它们修改类的字节码

## ClassFileTransformer

`ClassFileTransformer`接口是 Java Instrumentation API 的一部分, 它允许你在 Java 类被加载时对类字节码进行转换, 如插入跟踪代码、修改方法体、添加字段等。

`ClassFileTransformer`接口中只有两个方法：

```java
byte[] transform(ClassLoader loader, String className,
                 Class<?> classBeingRedefined, ProtectionDomain protectionDomain,
                 byte[] classfileBuffer);
byte[] transform(Module module, ClassLoader loader, String className,
                 Class<?> classBeingRedefined, ProtectionDomain protectionDomain,
                 byte[] classfileBuffer);
```

当类被加载时, JVM 会按照注册的顺序调用所有`ClassFileTransformer`的`transform`方法, 并传入相关的参数, 每个转换器接收的输入是前一个转换器输出的结果。`transform`方法的返回值是转换后的字节码数组, 如果返回`null`, 则表示不进行任何转换, 类将按原始字节码加载。

## MANIFEST.MF 文件

Java Agent 打成的 Jar 包中必须包含/META-INF/MANIFEST.MF 文件。

在 Java Agent 的 JAR 文件的`MANIFEST.MF`文件中, 至少需要定义以下两个属性之一:

1. `Premain-Class`：这个属性指定了包含`premain`方法的类。`premain`方法是在 JVM 启动时, 在应用程序的`main`方法执行之前调用的, 例如：

```
Premain-Class: com.example.MyAgent
```

2. `Agent-Class`：这个属性指定了包含`agentmain`方法的类。`agentmain`方法是在 JVM 启动后, 通过`Attach API`动态加载代理时调用的, 例如：

```
Agent-Class: com.example.MyAgent
```

如果 Java Agent 既要在 JVM 启动时加载, 也要在 JVM 运行时通过 Attach API 加载, 那么需要在`MANIFEST.MF`文件中同时定义`Premain-Class`和`Agent-Class`属性。

除了这两个必须的属性之外, 还有一些可选的属性：

- `Can-Redefine-Classes`：Java Agent 是否能够重新定义已经加载的类。默认值为`false`
- `Can-Retransform-Classes`：Java Agent 是否能够重新转换已经加载的类。默认值为`false`

例如, 一个简单的`MANIFEST.MF`文件可能如下所示：

```
Manifest-Version: 1.0
Premain-Class: com.example.MyAgent
Agent-Class: com.example.MyAgent
Can-Redefine-Classes: true
Can-Retransform-Classes: true
```
