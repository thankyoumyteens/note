# Java Agent

Java Agent 是一种“在 JVM 启动或运行过程中，插入你自己代码”的机制，用来在不改业务代码的情况下，对应用进行增强或监控。

它本质就是一个 特殊格式的 JAR 包，JVM 会在启动（或运行时 attach）时加载这个 JAR，调用里面特定的方法，并把一个叫 Instrumentation 的对象给你，你就可以：

- 拦截 / 修改类的加载过程
- 在类被加载前后对其字节码进行增强（通常配合 ASM / ByteBuddy 等）
- 做各种监控、埋点、性能收集、AOP 等

## Java Agent 怎么加载进 JVM

有两种常见方式：

1. 启动时加载（premain）
2. 运行时动态加载（agentmain）
