# main 函数

main 工作的重点是: 创建一个运行环境, 为接下来启动一个新的线程创建 JVM 并跳到 Java 主方法做好一切准备工作。

在 main 函数执行的最后一步, 程序将启动一个新的线程并将 Java 程序参数传递给它, 接下来阻塞自己, 并在新线程中继续执行。新线程也可称为为主线程, 它的执行入口是 JavaMain。

```c
// --- src/java.base/share/native/launcher/main.c --- //


```
