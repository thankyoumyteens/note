# 栈帧

_栈帧_ 用来存储数据和部分结果, 以及执行动态链接, 为方法返回值, 和分派异常。

每次调用方法都会创建一个新的栈帧。如果栈帧所属的方法执行完毕, 栈帧就会销毁, 无论方法是正常结束还是异常结束(抛出未捕获的异常)。栈帧在线程的 JVM 栈中分配。每个栈帧都有它自己的本地变量的数组(本地变量表, local variables), 和它自己的操作数栈(operand stack), 还有一个运行时常量池的引用, 这个运行时常量池是当前方法所属的类的运行时常量池。

栈帧可能会增加额外的执行信息, 比如调试信息。

本地变量数组和操作数栈的大小在编译时确定, 并且随着栈帧所属的方法的代码一起提供。因此栈帧数据结构的大小只会取决于 JVM 的实现, 并且这些结构的内存会在调用方法的同时被分配。

在任何时候, 一个线程只会有一个激活的栈帧, 这个栈帧是当前正在执行的方法的栈帧。这个栈帧被称为 _当前栈帧_, 这个栈帧所属的方法被称为 _当前方法_。这个方法所属的类称为 _当前类_。通常, JVM 操作的是当前栈帧的本地变量表和操作数栈。

如果一个栈帧所属的方法调用另一个方法, 或者执行完成, 这个栈帧就不是当前栈帧了。当一个方法执行时, 一个新的栈帧会被创建, 如果这个新方法获得控制权, 这个栈帧就成为当前栈帧。On method return, the current frame
passes back the result of its method invocation, if any, to the previous frame. The
current frame is then discarded as the previous frame becomes the current one.

Note that a frame created by a thread is local to that thread and cannot be referenced
by any other thread.

## Local Variables
