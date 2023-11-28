# Java 虚拟机栈

Java 虚拟机栈(Java Virtual Machine Stack)是线程私有的, 它的生命周期与线程相同。

Java 虚拟机栈有两种异常情况: 

1. 如果 Java 虚拟机栈容量设为固定大小, 当线程请求的栈深度大于虚拟机所允许的深度, 将抛出 StackOverflowError 异常
2. 如果 Java 虚拟机栈容量可以动态扩展, 当栈扩展时无法申请到足够的内存会抛出 OutOfMemoryError 异常
