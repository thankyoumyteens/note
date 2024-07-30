# Channel

NIO 是基于通道（Channel）和缓冲区（Buffer）进行操作，数据总是从 Channel 读取到 Buffer 中，或者从 Buffer 写入到 Channel 中。

常用的 Channel

- FileChannel：从文件中读写数据
- DatagramChannel：通过 UDP 读写网络中的数据
- SocketChannel：通过 TCP 读写网络中的数据
- ServerSocketChannel： 监听新进来的 TCP 连接

## FileChannel

```java
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

public class ChannelDemo {
    public static void main(String[] args) throws IOException {
        // 申请一块缓冲区
        ByteBuffer byteBuffer = ByteBuffer.allocate(1024);

        Path path = Paths.get("demo.txt");
        if (!Files.exists(path)) {
            Files.createFile(path);
        }

        {
            // 创建管道, 向文件中写数据
            FileChannel channel = FileChannel.open(path, StandardOpenOption.WRITE);

            // 先把数据写到buffer里
            byteBuffer.put("hello".getBytes());
            // 必须要从写模式切换到读模式, 把position设置为0, limit设置为position
            // 因为channel会从byteBuffer的position开始读取数据, 读取到limit为止
            byteBuffer.flip();

            // 再把数据写进channel
            int len = channel.write(byteBuffer);
            System.out.println(len);

            // 关闭chanel
            channel.close();
        }

        {
            // 创建管道, 从文件中读数据
            FileChannel channel = FileChannel.open(path, StandardOpenOption.READ);

            // 清空buffer
            // position设置为0, limit设置为capacity
            byteBuffer.clear();

            // 从channel读取数据到buffer
            int len = channel.read(byteBuffer);
            System.out.println(len);

            // 切换到读模式
            byteBuffer.flip();

            // 读取数据
            byte[] bytes = new byte[byteBuffer.limit()];
            byteBuffer.get(bytes);
            System.out.println(new String(bytes));

            // 关闭channel
            channel.close();
        }

    }
}
```

## ServerSocketChannel

```java
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;

public class SSChannelDemo {
    // 服务端
    public static void main(String[] args) throws IOException {
        // 申请一块缓冲区
        ByteBuffer byteBuffer = ByteBuffer.allocate(1024);

        // 创建管道, 接收客户端连接
        ServerSocketChannel channel = ServerSocketChannel.open();
        // 监听端口
        channel.socket().bind(new InetSocketAddress(27431));

        // 等待客户端的连接
        SocketChannel clientChannel = channel.accept();
        // 读取客户端发送的数据, 写入到buffer中
        clientChannel.read(byteBuffer);

        // 重置position, 准备读取
        byteBuffer.flip();

        // 读取buffer中的数据
        byte[] bytes = byteBuffer.array();

        // 打印数据
        System.out.println(new String(bytes, 0, byteBuffer.limit()));

        // 关闭chanel
        channel.close();
    }
}
```

## SocketChannel

```java
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;

public class SChannelDemo {
    // 客户端
    public static void main(String[] args) throws IOException {
        // 申请一块缓冲区
        ByteBuffer byteBuffer = ByteBuffer.allocate(1024);

        // 创建管道, 连接服务端
        SocketChannel channel = SocketChannel.open();
        // 连接服务端
        channel.connect(new InetSocketAddress("127.0.0.1", 27431));

        // 向buffer写入数据
        byteBuffer.put("hello".getBytes());

        // 重置position, 准备让channel读取
        byteBuffer.flip();

        // 读取buffer中的数据, 并发送给服务端
        channel.write(byteBuffer);

        // 关闭chanel
        channel.close();
    }
}
```
