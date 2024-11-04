# Oop-Klass 对象模型

一个 Klass 对象代表一个 Java 类。oop 指的是 Ordinary Object Pointer(普通对象指针), 它用来指向一个 Java 对象。

对于 oop 来说, 主要作用就是表示对象的实例数据, 没必要持有任何虚函数。而在描述 Java 类的 Klass 对象中含有 VTBL (虚方法表), 那么, Klass 就能够根据 Java 对象的实际类型进行分派, 这样一来, oop 只需要通过相应的 Klass 便可以找到所有的虚函数。这就避免了在每个对象中都分配一个 C++ VTBL 指针。
