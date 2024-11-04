# 对象的表示

JVM 没有对对象的内部数据结构做详细的要求。

In some of Oracle’s implementations of the Java Virtual Machine, a reference to a class
instance is a pointer to a _handle_ that is itself a pair of pointers: one to a table containing
the methods of the object and a pointer to the `Class` object that represents the type of the
object, and the other to the memory allocated from the heap for the object data.
