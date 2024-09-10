# Buffer

缓冲区本质上是一块可以写入数据, 然后可以从中读取数据的内存。这块内存被包装成 NIO Buffer 对象, 并提供了一组方法, 用来方便的访问该块内存。

当向 buffer 写入数据时, buffer 会记录下写了多少数据。一旦要读取数据, 需要通过 flip()方法将 Buffer 从写模式切换到读模式。在读模式下, 可以读取之前写入到 buffer 的所有数据。

一旦读完了所有的数据, 就需要清空缓冲区, 让它可以再次被写入。有两种方式能清空缓冲区: 调用 clear() 或 compact() 方法。clear()方法会清空整个缓冲区。compact()方法只会清除已经读过的数据。未读的数据被移到缓冲区的起始处, 新写入的数据将放到缓冲区未读数据的后面。

buffer 中有三个指针: 

- capacity: buffer 的容量, 一旦 Buffer 满了, 需要将其清空(通过读数据或者清除数据)才能继续往里写数据
- position: 当前的位置。初始的 position 值为 0。数据写到 Buffer 后, position 会向前移动一步。调用 flip 方法后, position 会被重置为 0。当从 position 处读取数据时, position 也会向前移动一步。position 最大是 capacity – 1
- limit: 限制可以从 Buffer 里读取多少数据(或者向 Buffer 里写取多少数据), 初始和 capacity 相等。调用 flip 方法后, limit 会被设置成当前的 position 值

## 常用的方法

- `put()`: 向 buffer 中写数据, 调用后, position 设置为写入的长度。比如 ByteBuffer, 写入 10 个字节后, position 从 0 变为 10
- `flip()`: 调用后, limit 设置为 position 的值, position 设置为 0
- `get()`: 从 buffer 中读数据, 调用后, position 设置为读取的长度。比如 ByteBuffer, 读取 5 个字节后, position 从 0 变为 5
- `clear()`: 调用后, limit 设置为 capacity 的值, position 设置为 0

## Buffer 的使用步骤

1. 调用 `put()` 写入数据
2. 调用 `flip()` 设置 position 和 limit
3. 使用 `get()` 读取数据

```java
import java.nio.Buffer;
import java.nio.ByteBuffer;

public class BufferDemo {
    public static void main(String[] args) {
        // 申请一块缓冲区
        ByteBuffer byteBuffer = ByteBuffer.allocate(1024);
        System.out.println("初始时" +
                ", position=" + byteBuffer.position() +
                ", limit=" + byteBuffer.limit() +
                ", capacity=" + byteBuffer.capacity());

        // 写入数据
        byteBuffer.put("hello".getBytes());
        System.out.println("写入数据后" +
                ", position=" + byteBuffer.position() +
                ", limit=" + byteBuffer.limit() +
                ", capacity=" + byteBuffer.capacity());

        // 调用flip
        byteBuffer.flip();
        System.out.println("调用flip后" +
                ", position=" + byteBuffer.position() +
                ", limit=" + byteBuffer.limit() +
                ", capacity=" + byteBuffer.capacity());

        // 读取数据
        byte[] bytes = new byte[byteBuffer.limit() / 2];
        byteBuffer.get(bytes);
        System.out.println("读取数据后" +
                ", position=" + byteBuffer.position() +
                ", limit=" + byteBuffer.limit() +
                ", capacity=" + byteBuffer.capacity());

        // 输出数据
        System.out.println(new String(bytes));

        // 调用flip
        byteBuffer.flip();
        System.out.println("调用flip后" +
                ", position=" + byteBuffer.position() +
                ", limit=" + byteBuffer.limit() +
                ", capacity=" + byteBuffer.capacity());

        // 读取数据
        bytes = new byte[byteBuffer.limit()];
        byteBuffer.get(bytes);
        System.out.println("读取数据后" +
                ", position=" + byteBuffer.position() +
                ", limit=" + byteBuffer.limit() +
                ", capacity=" + byteBuffer.capacity());
        // 输出数据
        System.out.println(new String(bytes));

    }
}
```

输出

```
初始时, position=0, limit=1024, capacity=1024
写入数据后, position=5, limit=1024, capacity=1024
调用flip后, position=0, limit=5, capacity=1024
读取数据后, position=2, limit=5, capacity=1024
he
调用flip后, position=0, limit=2, capacity=1024
读取数据后, position=2, limit=2, capacity=1024
he
```
