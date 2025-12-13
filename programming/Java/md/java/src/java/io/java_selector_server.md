# 实现一个简单的服务器(收到什么就返回什么)

```java
package com.example;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.util.Iterator;
import java.util.Set;

public class NioEchoServer {
    static void main(String[] args) throws IOException {
        // 1. 创建 Selector
        Selector selector = Selector.open();

        // 2. 创建 ServerSocketChannel, 监听 8080 端口
        ServerSocketChannel serverChannel = ServerSocketChannel.open();
        serverChannel.bind(new InetSocketAddress(8080));
        serverChannel.configureBlocking(false); // 非阻塞

        // 3. 把 serverChannel 注册到 selector，关心“接受连接”事件(OP_ACCEPT)
        serverChannel.register(selector, SelectionKey.OP_ACCEPT);

        System.out.println("NIO Echo Server started on port 8080...");

        // 创建 buffer
        ByteBuffer buffer = ByteBuffer.allocate(1024);

        // 4. 事件循环
        while (true) {
            // 阻塞等待至少一个事件准备就绪
            selector.select();

            // 拿到所有就绪的事件 key
            Set<SelectionKey> selectedKeys = selector.selectedKeys();
            Iterator<SelectionKey> it = selectedKeys.iterator(); // 拿到迭代器

            while (it.hasNext()) {
                SelectionKey key = it.next();
                it.remove(); // 必须移除，否则下次还会处理

                if (key.isAcceptable()) {
                    // 5. 有新的客户端连接进来了
                    ServerSocketChannel ssc = (ServerSocketChannel) key.channel();
                    SocketChannel clientChannel = ssc.accept();
                    clientChannel.configureBlocking(false);

                    System.out.println("Client connected: " + clientChannel.getRemoteAddress());

                    // 关心“读数据”事件
                    clientChannel.register(selector, SelectionKey.OP_READ);

                } else if (key.isReadable()) {
                    // 6. 某个客户端有数据可读
                    SocketChannel clientChannel = (SocketChannel) key.channel();
                    buffer.clear();

                    int read = clientChannel.read(buffer);
                    if (read == -1) {
                        // 客户端断开
                        System.out.println("Client disconnected: " + clientChannel.getRemoteAddress());
                        clientChannel.close();
                        continue;
                    }

                    // 由写模式切换到读模式
                    buffer.flip();
                    byte[] bytes = new byte[buffer.remaining()];
                    buffer.get(bytes);
                    String msg = new String(bytes);

                    // 输出接收到的数据
                    System.out.println("Received: " + msg.trim());

                    // 回显给客户端
                    buffer.clear();
                    buffer.put(("echo: " + msg).getBytes());
                    buffer.flip();
                    clientChannel.write(buffer);
                }
            }
        }
    }
}
```

## 测试这个服务

```sh
# 安装 brew install telnet
telnet 127.0.0.1 8080

# 连上后, 在终端里随便输入一行, 就会收到服务端的回显
```
