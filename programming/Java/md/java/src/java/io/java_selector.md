# Selector

Selector 是 Java NIO 中实现多路复用的关键，可以基于 selector 对象实现一个线程管理多个 channel, 避免线程之间上下文切换带来的开销, 减少多个线程占用的系统资源。

使用步骤

1. 创建 selector
2. 向 selector 中注册 channel, 并监听指定的事件
3. 询式获取 selector 中已经就绪的事件并处理

## 服务端

```java
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.util.Iterator;
import java.util.Set;

public class SSSelectorDemo {
    // 服务端
    public static void main(String[] args) throws IOException {
        // 申请一块缓冲区
        ByteBuffer byteBuffer = ByteBuffer.allocate(1024);

        // 创建管道, 接收客户端连接
        ServerSocketChannel channel = ServerSocketChannel.open();
        // 设置为非阻塞
        channel.configureBlocking(false);
        // 监听端口
        channel.bind(new InetSocketAddress(27431));

        // 创建selector
        Selector selector = Selector.open();
        // 向selector中注册channel, 并监听连接就绪事件
        channel.register(selector, SelectionKey.OP_ACCEPT);

        while (true) {
            // 查询是否有就绪的事件,
            // 并把就绪的事件设置到publicSelectedKeys中
            int selectedKeyCount = selector.select();
            if (selectedKeyCount <= 0) {
                continue;
            }

            // 获取publicSelectedKeys中的就绪事件
            Set<SelectionKey> selectionKeys = selector.selectedKeys();

            // 遍历所有就绪的事件
            Iterator<SelectionKey> iterator = selectionKeys.iterator();
            while (iterator.hasNext()) {
                SelectionKey next = iterator.next();
                // 判断是就绪的是什么事件
                if (next.isAcceptable()) {
                    // 是连接就绪事件, 则获取客户端的连接
                    //     连接就绪事件同一个客户端只会触发一次
                    //     但是读就绪事件可能触发多次
                    //     所以这里不能用 try-with-resource
                    //     避免客户端连接被自动关闭
                    SocketChannel clientChannel = channel.accept();
                    // 把客户端的连接设置为非阻塞
                    clientChannel.configureBlocking(false);
                    // 把客户端的channel注册到selector, 并监听读就绪事件
                    clientChannel.register(selector, SelectionKey.OP_READ);
                } else if (next.isReadable()) {
                    // 是读就绪事件, 则读取客户端发送的数据
                    SocketChannel clientChannel = (SocketChannel) next.channel();
                    int len;
                    while ((len = clientChannel.read(byteBuffer)) > 0) {
                        // 重置position
                        byteBuffer.flip();
                        // 打印数据
                        System.out.println(new String(byteBuffer.array(), 0, len));
                        // 清空buffer, 准备继续读取
                        byteBuffer.clear();
                    }
                }
                // 需要手动删掉处理过的事件
                iterator.remove();
            }
        }
    }
}
```
