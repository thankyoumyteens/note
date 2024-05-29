# Buffer

Java的Buffer类是一个抽象类, 对应于Java的主要数据类型, 在NIO中有8种Buffer冲区类: ByteBuffer、CharBuffer、DoubleBuffer、FloatBuffer、IntBuffer、LongBuffer、ShortBuffer、MappedByteBuffe。前7种Buffer类型, 覆盖了能在IO中传输的所有的Java基本数据类型。第8种类型MappedByteBuffer是专门用于内存映射的一种ByteBuffer类型。Buffer类是一个非线程安全类。

Buffer类内部, 有一个byte[]数组作为内存缓冲区。

## capacity属性

capacity属性表示Buffer容量的大小。一旦写入的对象数量超过了capacity, 缓冲区就不能再写入了。capacity容量指的是写入的数据对象的数量。例如使用DoubleBuffer, 如果其caplacity是100, 那么最多可以写入100个double数据。

Buffer类的对象在初始化时, 会按照capacity分配内部的内存。capacity属性一旦初始化, 就不能再改变。

## position属性

position属性表示当前的位置。position属性与缓冲区的读写模式有关。在不同的模式下, position属性的值是不同的。当读写的模式改变时, position会进行调整。

写模式: 

1. 在刚进入到写模式时, position值为0, 表示当前的写入位置为从头开始
2. 每当一个数据写到缓冲区之后, position会向后移动到下一个可写的位置
3. 初始的position值为0, 最大可写值position为limit-1

读模式: 

1. 当缓冲区刚开始进入到读模式时, position会被重置为0
2. 当从缓冲区读取时, 也是从position位置开始读。读取数据后, position向前移动到下一个可读的位置
3. position最大的值为最limit

## limit属性

limit属性表示读写的最大上限。limit属性也与缓冲区的读写模式有关。在不同的模式下, limit的值含义不同。

写模式: 

1. 在写模式下, limit属性表示可以写入的数据最大上限。在刚进入到写模式时, limit的值会被设置成capacity, 表示可以一直将缓冲区的容量写满

读模式: 

1. 在读模式下, limit的值表示最多能从缓冲区中读取到多少数据

从写模式切换到读模式: 将写模式下的position值, 设置成读模式下的limit值, 也就是说, 将之前写入的最大数量, 作为可以读取的上限。同时, 新的position会被重置为0, 表示可以从0开始读。

## mark属性

mark属性用于暂存position属性的值, 可以将当前的position临时存入mark中, 需要的时候可以再从mark中恢复到position位置。

