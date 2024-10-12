# 运行时数据区

JVM 定义了各种运行时数据区用来运行程序。一部分数据区在 JVM 启动时创建, 并在 JVM 结束运行时销毁。其它的数据区是每个线程各有一份。线程私有的数据区是在线程创建时创建, 并在线程终止时销毁。

## PC 寄存器

JVM 支持许多线程同时执行。每个 JVM 线程有它自己的 `pc` (program counter) 寄存器。在任何时刻, 每个 JVM 线程只会执行一个方法中的代码, 这个方法就是该线程的当前方法。如果当前方法不是 `native` 的, `pc` 寄存器的值就是当前正在被执行的 JVM 指令的地址。如果当前方法是 `native` 的, `pc` 寄存器的值是未定义的。JVM 的 `pc` 寄存器的宽度足以容纳 `returnAddress` 或一个特定平台上的本地指针。

## Java Virtual Machine Stacks

每个 JVM 线程都有一个私有的 JVM 栈, JVM 栈和线程同时创建。JVM 栈中存储的是栈帧。JVM 栈和传统编程语言(比如 C 语言)的栈类似: 它持有局部变量和中间结果, 并在方法的调用和返回中发挥作用。由于除了压入和弹出栈帧之外，JVM 栈从来不会被直接操作，所以在具体实现上可能会选择在堆内存中分配栈帧，而不是在传统意义上的栈内存中分配。JVM 栈空间的内存不需要是连续的。

在第一版的 JVM 规范中, JVM 栈被称为 Java 栈。

本规范既允许 JVM 栈使用固定大小, 也允许栈的大小根据计算需要动态地扩展和收缩。如果 JVM 栈的大小固定, 那么每个 JVM 栈的大小都可以在创建时单独指定。

一个 JVM 实现可以让程序员或用户控制 JVM 栈的初始大小, 对于可以动态扩展和收缩的 JVM 栈, 可以控制栈容量的最大值和最小值。

以下是和 JVM 栈相关的异常情况:

- 如果线程请求的栈容量超过了 JVM 栈允许的大小, JVM 会抛出 `StackOverflowError`
- 如果 JVM 栈可以动态扩展, 并且没有足够的内存空间来完成扩展, 或者连为一个新的线程创建 JVM 栈的空间都没有了, JVM 会抛出 `OutOfMemoryError`

## Heap

JVM 有一个所有 JVM 线程共享的 _堆_。 堆是用来给所有的对象和数组分配内存的运行时数据区。

堆在 JVM 启动时被创建。堆中存储的对象会被自动内存管理系统(被称为 _垃圾回收器_)回收(reclaimed); 对象从不会被显式地释放。JVM 的设计并不依赖于某一种特定的垃圾回收或内存管理机制，它可以与各种不同的自动内存管理技术一起工作, 并且可以根据不同的 JVM 实现的要求选择不同的内存管理技术。堆的大小可以是固定的, 也可以是动态扩展的, 并且可以收缩用不到的堆空间。堆空间的内存不需要是连续的。

一个 JVM 实现可以让程序员或用户控制堆的初始大小, 对于可以动态扩展和收缩的堆, 可以控制堆空间的最大值和最小值。

以下是和堆相关的异常情况:

- 如果请求的堆大小超过了自动内存管理系统允许的大小, JVM 会抛出 `OutOfMemoryError`

## Method Area

JVM 的 _方法区_ 是所有 JVM 线程共享的。方法区类似于传统编程语言中存储编译后的代码的区域, 或者类似于操作系统中进程的代码段。这里存储着每个类的结构, 例如运行时常量池, 字段和方法的数据, 方法和构造器的代码, 包括类和接口初始化以及实例初始化中使用的特殊方法。

方法区在 JVM 启动时创建。尽管方法区在逻辑上是堆的一部分, 但是简单的 JVM 实现可能不会对其进行垃圾回收或空间压缩。本规范并不指定方法区的实现位置, 或者已编译代码的管理策略。方法区可以是固定大小, 也可以动态扩展和收缩。方法区的内存不需要是连续的。

一个 JVM 实现可以让程序员或用户控制方法区的初始大小, 对于可以动态扩展和收缩的方法区, 可以控制方法区的最大值和最小值。

以下是和方法区相关的异常情况:

- 如果方法区的可用空间大小不满足一个新的分配请求, JVM 会抛出 `OutOfMemoryError`

## Run-Time Constant Pool

一个 _运行时常量池_ 是一个类(或者接口)对 `.class` 文件中常量池的运行时表示。它包含几种常量, 范围从 "在编译时已知的数值字面量" 到 "必须在运行时解析的方法和字段的引用"。运行时常量池提供的功能类似于传统编程语言的符号表, 但是比起典型的符号表, 运行时常量池有更宽的数据范围。

Each run-time constant pool is allocated from the Java Virtual Machine's method
area. The run-time constant pool for a class or interface is constructed
when the class or interface is created by the Java Virtual Machine.

The following exceptional condition is associated with the construction of the run-time constant pool for a class or interface:

- When creating a class or interface, if the construction of the run-time constant pool requires more memory than can be made available in the method area of the Java Virtual Machine, the Java Virtual Machine throws an `OutOfMemoryError`

## Native Method Stacks

An implementation of the Java Virtual Machine may use conventional stacks,
colloquially called "C stacks," to support `native` methods (methods written in a
language other than the Java programming language). Native method stacks may
also be used by the implementation of an interpreter for the Java Virtual Machine's
instruction set in a language such as C. Java Virtual Machine implementations
that cannot load `native` methods and that do not themselves rely on conventional
stacks need not supply native method stacks. If supplied, native method stacks are
typically allocated per thread when each thread is created.

This specification permits native method stacks either to be of a fixed size or to
dynamically expand and contract as required by the computation. If the native
method stacks are of a fixed size, the size of each native method stack may be
chosen independently when that stack is created.

A Java Virtual Machine implementation may provide the programmer or the user control
over the initial size of the native method stacks, as well as, in the case of varying-size native
method stacks, control over the maximum and minimum method stack sizes.

The following exceptional conditions are associated with native method stacks:

- If the computation in a thread requires a larger native method stack than is permitted, the Java Virtual Machine throws a `StackOverflowError`
- If native method stacks can be dynamically expanded and native method stack expansion is attempted but insufficient memory can be made available, or if insufficient memory can be made available to create the initial native method stack for a new thread, the Java Virtual Machine throws an `OutOfMemoryError`
