# 栈帧

_栈帧_ 用来存储数据和部分结果, 以及执行动态链接, 为方法返回值, 和分派异常。

每次调用方法都会创建一个新的栈帧。如果栈帧所属的方法执行完毕, 栈帧就会销毁, 无论方法是正常结束还是异常结束(抛出未捕获的异常)。栈帧在线程的 JVM 栈中分配。每个栈帧都有它自己的本地变量的数组(本地变量表, local variables), 和它自己的操作数栈(operand stack), 还有一个运行时常量池的引用, 这个运行时常量池是当前方法所属的类的运行时常量池。

栈帧可能会增加额外的执行信息, 比如调试信息。

本地变量数组和操作数栈的大小在编译时确定, 并且随着栈帧所属的方法的代码一起提供。因此栈帧数据结构的大小只会取决于 JVM 的实现, 并且这些结构的内存会在调用方法的同时被分配。

在任何时候, 一个线程只会有一个激活的栈帧, 这个栈帧是当前正在执行的方法的栈帧。这个栈帧被称为 _当前栈帧_, 这个栈帧所属的方法被称为 _当前方法_。这个方法所属的类称为 _当前类_。通常, JVM 操作的是当前栈帧的本地变量表和操作数栈。

如果一个栈帧所属的方法调用另一个方法, 或者执行完成, 这个栈帧就不是当前栈帧了。当一个方法执行时, 一个新的栈帧会被创建, 如果这个新方法获得控制权, 这个栈帧就成为当前栈帧。在方法返回时, 当前栈帧会回传方法的执行结果, 如果有的话, 传回给上一个栈帧。然后, 丢弃当前栈帧, 上一个栈帧成为新的当前栈帧。

注意, 一个线程创建的栈帧是线程本地的, 任何线程都不能引用另一个线程的栈帧。

## Local Variables

每个栈帧内部都有一个变量的数组, 称为它的 _本地变量表_。The length of the local variable array of a frame is determined at compile-time and
supplied in the binary representation of a class or interface along with the code for
the method associated with the frame.

A single local variable can hold a value of type `boolean`, `byte`, `char`, `short`, `int`,
`float`, `reference`, or `returnAddress`. A pair of local variables can hold a value
of type `long` or `double`.

Local variables are addressed by indexing. The index of the first local variable is
zero. An integer is considered to be an index into the local variable array if and only
if that integer is between zero and one less than the size of the local variable array.

A value of type `long` or type `double` occupies two consecutive local variables.
Such a value may only be addressed using the lesser index. For example, a value of
type `double` stored in the local variable array at index n actually occupies the local
variables with indices n and n+1; however, the local variable at index n+1 cannot
be loaded from. It can be stored into. However, doing so invalidates the contents
of local variable n.

The Java Virtual Machine does not require n to be even. In intuitive terms, values
of types `long` and `double` need not be 64-bit aligned in the local variables array.
Implementors are free to decide the appropriate way to represent such values using
the two local variables reserved for the value.

The Java Virtual Machine uses local variables to pass parameters on method
invocation. On class method invocation, any parameters are passed in consecutive
local variables starting from local variable 0. On instance method invocation,
local variable 0 is always used to pass a reference to the object on which the
instance method is being invoked (`this` in the Java programming language). Any
parameters are subsequently passed in consecutive local variables starting from
local variable 1.
