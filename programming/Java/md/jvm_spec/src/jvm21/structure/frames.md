# 栈帧

_栈帧_ 用来存储数据和部分结果, 以及执行动态链接, 为方法返回值, 和分派异常。

每次调用方法都会创建一个新的栈帧。如果栈帧所属的方法执行完毕, 栈帧就会销毁, 无论方法是正常结束还是异常结束(抛出未捕获的异常)。栈帧在线程的 JVM 栈中分配。每个栈帧都有它自己的本地变量的数组(本地变量表, local variables), 和它自己的操作数栈(operand stack), 还有一个运行时常量池的引用, 这个运行时常量池是当前方法所属的类的运行时常量池。

栈帧可能会增加额外的执行信息, 比如调试信息。

本地变量数组和操作数栈的大小在编译时确定, 并且随着栈帧所属的方法的代码一起提供。因此栈帧数据结构的大小只会取决于 JVM 的实现, 并且这些结构的内存会在调用方法的同时被分配。

在任何时候, 一个线程只会有一个激活的栈帧, 这个栈帧是当前正在执行的方法的栈帧。这个栈帧被称为 _当前栈帧_, 这个栈帧所属的方法被称为 _当前方法_。这个方法所属的类称为 _当前类_。通常, JVM 操作的是当前栈帧的本地变量表和操作数栈。

如果一个栈帧所属的方法调用另一个方法, 或者执行完成, 这个栈帧就不是当前栈帧了。当一个方法执行时, 一个新的栈帧会被创建, 如果这个新方法获得控制权, 这个栈帧就成为当前栈帧。在方法返回时, 当前栈帧会回传方法的执行结果, 如果有的话, 传回给上一个栈帧。然后, 丢弃当前栈帧, 上一个栈帧成为新的当前栈帧。

注意, 一个线程创建的栈帧是线程本地的, 任何线程都不能引用另一个线程的栈帧。

## Local Variables

每个栈帧内部都有一个变量的数组, 称为它的 _本地变量表_。一个栈帧中本地变量数组的长度是在编译时就确定的, 并且随着 .class 文件的方法中的 code 属性一起提供。

一个本地变量可以保存一个 `boolean`, `byte`, `char`, `short`, `int`, `float`, `reference`, 或 `returnAddress` 类型的值。一对(两个)本地变量可以保存一个 `long` 或 `double` 类型的值。

本地变量表按索引编址。第 1 个本地变量的索引是 0。如果一个整数的范围在 0 到本地变量数组长度的范围内, 它就被认为是本地变量数组的索引。

一个 `long` 或 `double` 类型的值占用两个连续的本地变量。这种值的索引使用的是较小的索引值。例如, 一个 `double` 类型的值存储在本地变量数组索引为 n 的位置, 但它实际占用的索引是 n 和 n+1; 但是索引 n+1 的本地变量是不能读取, 只能存储的。然而, 这样做(指的是向索引 n+1 中存储新的本地变量)会使索引为 n 的本地变量失效。

JVM 不要求 n 是偶数。用直观的术语来说, `long` 和 `double` 类型的值在本地变量数组中不需要按 64 位对齐。JVM 实现者可以自由决定以哪种适合的方式用两个本地变量来保存这两种类型的值。

The Java Virtual Machine uses local variables to pass parameters on method
invocation. On class method invocation, any parameters are passed in consecutive
local variables starting from local variable 0. On instance method invocation,
local variable 0 is always used to pass a reference to the object on which the
instance method is being invoked (`this` in the Java programming language). Any
parameters are subsequently passed in consecutive local variables starting from
local variable 1.

## Operand Stacks

Each frame contains a last-in-first-out (LIFO) stack known as its _operand stack_. The maximum depth of the operand stack of a frame is determined at
compile-time and is supplied along with the code for the method associated with
the frame.

Where it is clear by context, we will sometimes refer to the operand stack of the
current frame as simply the operand stack.

The operand stack is empty when the frame that contains it is created. The
Java Virtual Machine supplies instructions to load constants or values from local
variables or fields onto the operand stack. Other Java Virtual Machine instructions
take operands from the operand stack, operate on them, and push the result back
onto the operand stack. The operand stack is also used to prepare parameters to be
passed to methods and to receive method results.

For example, the _iadd_ instruction adds two `int` values together. It requires
that the `int` values to be added be the top two values of the operand stack, pushed
there by previous instructions. Both of the `int` values are popped from the operand
stack. They are added, and their sum is pushed back onto the operand stack.
Subcomputations may be nested on the operand stack, resulting in values that can
be used by the encompassing computation.

Each entry on the operand stack can hold a value of any Java Virtual Machine type,
including a value of type `long` or type `double`.

Values from the operand stack must be operated upon in ways appropriate to their
types. It is not possible, for example, to push two `int` values and subsequently treat
them as a `long` or to push two `float` values and subsequently add them with an
_iadd_ instruction. A small number of Java Virtual Machine instructions (the _dup_
instructions and _swap_) operate on run-time data areas as raw values
without regard to their specific types; these instructions are defined in such a way
that they cannot be used to modify or break up individual values. These restrictions
on operand stack manipulation are enforced through `class` file verification.

At any point in time, an operand stack has an associated depth, where a value of
type `long` or `double` contributes two units to the depth and a value of any other
type contributes one unit.

## Dynamic Linking
