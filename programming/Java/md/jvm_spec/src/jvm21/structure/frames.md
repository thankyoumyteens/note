# 栈帧

_栈帧_ 用来存储数据和部分结果, 以及执行动态链接, 为方法返回值, 和分派异常。

每次调用方法都会创建一个新的栈帧。如果栈帧所属的方法执行完毕, 栈帧就会销毁, 无论方法是正常结束还是异常结束(抛出未捕获的异常)。栈帧在线程的 JVM 栈中分配。每个栈帧都有它自己的本地变量的数组(本地变量表, local variables), 和它自己的操作数栈(operand stack), 还有一个运行时常量池的引用, 这个运行时常量池是当前方法所属的类的运行时常量池。

栈帧可能会增加额外的执行信息, 比如调试信息。

本地变量数组和操作数栈的大小 are determined at
compile-time and are supplied along with the code for the method associated with
the frame. Thus the size of the frame data structure depends only on the
implementation of the Java Virtual Machine, and the memory for these structures
can be allocated simultaneously on method invocation.

Only one frame, the frame for the executing method, is active at any point in a given
thread of control. This frame is referred to as the _current frame_, and its method is
known as the _current method_. The class in which the current method is defined is
the _current class_. Operations on local variables and the operand stack are typically
with reference to the current frame.

A frame ceases to be current if its method invokes another method or if its method
completes. When a method is invoked, a new frame is created and becomes current
when control transfers to the new method. On method return, the current frame
passes back the result of its method invocation, if any, to the previous frame. The
current frame is then discarded as the previous frame becomes the current one.

Note that a frame created by a thread is local to that thread and cannot be referenced
by any other thread.

## Local Variables
