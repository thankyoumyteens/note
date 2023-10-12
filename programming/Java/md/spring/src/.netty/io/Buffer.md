# Buffer

Java的Buffer类是一个抽象类，对应于Java的主要数据类型，在NIO中有8种Buffer冲区类：ByteBuffer、CharBuffer、DoubleBuffer、FloatBuffer、IntBuffer、LongBuffer、ShortBuffer、MappedByteBuffe。前7种Buffer类型，覆盖了能在IO中传输的所有的Java基本数据类型。第8种类型MappedByteBuffer是专门用于内存映射的一种ByteBuffer类型。Buffer类是一个非线程安全类。

Buffer类内部，有一个byte[]数组作为内存缓冲区。

## capacity属性

Buffer类的capacity属性，表示内部容量的大小。一旦写入的对象数量超过了capacity，缓冲区就满了，不能再写入了。

Buffer类的对象在初始化时，会按照capacity分配内部的内存。capacity属性一旦初始化，就不能再改变。

capacity容量指的是写入的数据对象的数量。例如使用DoubleBuffer，如果其caplacity是100，那么最多可以写入100个double数据。

## position属性

