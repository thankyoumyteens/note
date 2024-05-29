# JVMTI

JVM 是不允许在运行时动态重载一个类的, 这表示 Javassist 和 ASM 修改的类需要在原本的类加载之前先被加载。如果要修改已经被 JVM 加载的类, 可以结合 JVMTI 技术一起使用。

JVM 工具接口(JVM Tool Interface, JVMTI)可以用来实现 profiling 性能分析、debug、监控、线程分析、覆盖率分析等功能, 可以在不改动代码的情况下监控、分析 java 进程的状态等。
