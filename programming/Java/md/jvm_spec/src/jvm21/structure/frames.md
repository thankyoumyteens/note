# 栈帧

_栈帧_ 用来存储数据和部分结果, 以及执行动态链接, 为方法返回值, 和分派异常。

每次调用方法都会创建一个新的栈帧。如果栈帧所属的方法执行完毕, 栈帧就会销毁, 无论方法是正常结束还是异常结束(抛出未捕获的异常)。栈帧在线程的 JVM 栈中分配。每个栈帧都有它自己的本地变量的数组(本地变量表, local variables), 和它自己的操作数栈(operand stack), 还有一个运行时常量池的引用, 这个运行时常量池是当前方法所属的类的运行时常量池。

栈帧可能会增加额外的执行信息, 比如调试信息。

本地变量数组和操作数栈的大小在编译时确定, 并且随着栈帧所属的方法的代码一起提供。因此栈帧数据结构的大小只会取决于 JVM 的实现, 并且这些结构的内存会在调用方法的同时被分配。

在任何时候, 一个线程只会有一个激活的栈帧, 这个栈帧是当前正在执行的方法的栈帧。这个栈帧被称为 _当前栈帧_, 这个栈帧所属的方法被称为 _当前方法_。这个方法所属的类称为 _当前类_。通常, JVM 操作的是当前栈帧的本地变量表和操作数栈。

如果一个栈帧所属的方法调用另一个方法, 或者执行完成, 这个栈帧就不是当前栈帧了。当一个方法执行时, 一个新的栈帧会被创建, 如果这个新方法获得控制权, 这个栈帧就成为当前栈帧。在方法返回时, 当前栈帧会回传方法的执行结果, 如果有的话, 传回给上一个栈帧。然后, 丢弃当前栈帧, 上一个栈帧成为新的当前栈帧。

注意, 一个线程创建的栈帧是线程本地的, 任何线程都不能引用另一个线程的栈帧。

## Local Variables

每个栈帧内部都有一个变量的数组, 称为这个栈帧的 _本地变量表_。一个栈帧中本地变量数组的长度是在编译时就确定的, 并且随着 `class` 文件的方法中的 code 属性一起提供。

一个本地变量可以保存一个 `boolean`, `byte`, `char`, `short`, `int`, `float`, `reference`, 或 `returnAddress` 类型的值。一对(两个)本地变量可以保存一个 `long` 或 `double` 类型的值。

本地变量表按索引编址。第 1 个本地变量的索引是 0。如果一个整数的范围在 0 到本地变量数组长度的范围内, 它就被认为是本地变量数组的索引。

一个 `long` 或 `double` 类型的值占用两个连续的本地变量。这种值的索引使用的是较小的索引值。例如, 一个 `double` 类型的值存储在本地变量数组索引为 n 的位置, 但它实际占用的索引是 n 和 n+1; 但是索引 n+1 的本地变量是不能读取, 只能存储的。然而, 这样做(指的是向索引 n+1 中存储新的本地变量)会使索引为 n 的本地变量失效。

JVM 不要求 n 是偶数。用直观的术语来说, `long` 和 `double` 类型的值在本地变量数组中不需要按 64 位对齐。JVM 实现者可以自由决定以哪种适合的方式用两个本地变量来保存这两种类型的值。

JVM 在方法调用时, 使用本地变量表来传递参数。在类方法调用时, 所有参数都连续存放在从 0 开始的本地变量表中。在实例方法调用时,
本地变量 0 总是用来传递调用方法所属的对象的引用(就是 Java 语言里的 `this`), 然后其它参数从 1 开始存放。

## Operand Stacks

每个栈帧内部都有一个 后入先出(LIFO) 的栈, 称为这个栈帧的 _操作数栈_。一个栈帧中操作数栈的最大深度是在编译时就确定的, 并且随着 `class` 文件的方法中的 code 属性一起提供。

在上下文清晰的情况下，我们有时会简单地将 当前栈帧的操作数栈 直接称为 操作数栈。

栈帧创建时, 操作数栈是空的。JVM 提供了把常量或值从本地变量表或字段中加载到操作数栈的指令。其它 JVM 指令从操作数栈中取出操作数, 执行操作, 然后把结果放回操作数栈。操作数栈也可以用来给方法传递参数和接收方法的返回值。

例如, _iadd_ 指令把两个 `int` 值相加。它要求两个要相加的 `int` 值在操作数栈的栈顶, 这两个值由 _iadd_ 指令之前的其它指令推入(push)操作数栈。两个 `int` 值会被 _iadd_ 指令从操作数栈中弹出(pop)。把两个值相加, 并把相加的结果推入操作数栈。子计算可以被嵌套在操作数栈上，从而产生能够被更高层计算所使用的值。

操作数栈上的每一项都能保存任意一个 JVM 类型, 包括 `long` 或 `double` 类型的值。

操作数栈上值必须执行符合它们类型的操作。下面这种情况是不可能的: 推入两个 `int` 值然后把它们当作 `long` 类型, 或者推入两个 `float` 值然后对它们使用 _iadd_ 指令。一小部分 JVM 指令 (_dup_ 和 _swap_) 操作的是运行时数据区的原始值不关心它们的具体值; 这些指令定义为不能修改或分解独立的值。这些对操作数栈操作的限制是通过 `class` 文件验证来强制执行的。

在任何时候, `long` 或 `double` 类型值占用两个单位的栈深度, 其它类型值占用一个单位的栈深度。

## Dynamic Linking

每个栈帧内部都有一个指向运行时常量池中当前方法的引用, 来支持方法代码的 _动态链接_。`class` 文件中的方法代码用过符号引用(symbolic references)指向了当前方法要执行的其他方法和要访问的变量。动态链接把这些符号引用翻译成具体的方法引用, 根据需要加载某些类去解析尚未定义的符号, 把访问的变量的符号引用翻译成它们运行时存储结构中的偏移量。

通过对用到的方法和变量的后期绑定, 就算本方法所使用到的其他类中进行了更改, 也不会影响本方法的代码。

## Normal Method Invocation Completion

一个方法的调用如果没有抛出异常(不管是 JVM 直接抛出还是通过 `throw` 语句显式抛出), 就是 _正常完成_。如果当前方法正常执行完成, 随后可能会有一个返回值给调用方。当调用的方法执行了返回指令, 就会有返回值, 调用的返回指令需要符合返回值的类型。

在这种情况下, 当前栈帧要用来恢复调用方的状态, 包括它的本地变量表和操作数栈, with the program counter of the
invoker appropriately incremented to skip past the method invocation instruction.
Execution then continues normally in the invoking method's frame with the
returned value (if any) pushed onto the operand stack of that frame.

## Abrupt Method Invocation Completion

A method invocation _completes abruptly_ if execution of a Java Virtual Machine
instruction within the method causes the Java Virtual Machine to throw an
exception, and that exception is not handled within the method. Execution
of an _athrow_ instruction also causes an exception to be explicitly thrown
and, if the exception is not caught by the current method, results in abrupt method
invocation completion. A method invocation that completes abruptly never returns
a value to its invoker.
