# Socket

网络通信是基于 Socket 实现的, 可以实现不同设备间的通信。

## 服务端

```java
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.Iterator;
import java.util.Set;

public class ServerDemo {
    public static void main(String[] args) {
        // 服务端
        new Thread(() -> {
            try {
                // 发送数据的缓冲区
                ByteBuffer sendBuf = ByteBuffer.allocate(1024);
                // 接收数据的缓冲区
                ByteBuffer receiveBuf = ByteBuffer.allocate(1024);
                ServerSocketChannel channel = ServerSocketChannel.open();
                Selector selector = Selector.open();
                channel.bind(new InetSocketAddress(27431));
                channel.configureBlocking(false);
                channel.register(selector, SelectionKey.OP_ACCEPT);
                while (true) {
                    int fdCount = selector.select();
                    if (fdCount <= 0) {
                        continue;
                    }
                    Set<SelectionKey> selectionKeys = selector.selectedKeys();
                    Iterator<SelectionKey> iterator = selectionKeys.iterator();
                    while (iterator.hasNext()) {
                        SelectionKey key = iterator.next();

                        if (key.isAcceptable() && key.isValid()) {
                            // 连接事件
                            SocketChannel clientChannel = channel.accept();
                            clientChannel.configureBlocking(false);
                            clientChannel.register(selector, SelectionKey.OP_READ);
                        } else if (key.isReadable() && key.isValid()) {
                            // 读事件
                            SocketChannel c = (SocketChannel) key.channel();
                            receiveBuf.clear();
                            int len = c.read(receiveBuf);
                            if (len > 0) {
                                System.out.println("收到了: ");
                                String msg = new String(receiveBuf.array(), 0, len);
                                System.out.println(msg);
                            }
                            sendBuf.clear();
                            sendBuf.put("服务端消息".getBytes());
                            sendBuf.flip();
                            c.write(sendBuf);
                        }

                        iterator.remove();
                    }
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }).start();
    }
}
```

## 客户端

```java
package org.example.threadsdemo;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.util.Iterator;
import java.util.Set;

public class ClientDemo {
    public static void main(String[] args) {
        // 客户端
        new Thread(() -> {
            try {
                // 发送数据的缓冲区
                ByteBuffer sendBuf = ByteBuffer.allocate(1024);
                // 接收数据的缓冲区
                ByteBuffer receiveBuf = ByteBuffer.allocate(1024);
                Selector selector = Selector.open();
                SocketChannel channel = SocketChannel.open();
                channel.configureBlocking(false);
                channel.connect(new InetSocketAddress("127.0.0.1", 27431));
                channel.register(selector, SelectionKey.OP_CONNECT);
                while (true) {
                    // 准备好的文件描述符的个数
                    int fdCount = selector.select();
                    if (fdCount <= 0) {
                        continue;
                    }
                    Set<SelectionKey> selectionKeys = selector.selectedKeys();
                    Iterator<SelectionKey> iterator = selectionKeys.iterator();
                    if (iterator.hasNext()) {
                        SelectionKey key = iterator.next();

                        if (key.isConnectable() && key.isValid()) {
                            // 连接事件
                            SocketChannel c = (SocketChannel) key.channel();
                            if (c.isConnectionPending()) {
                                // 完成连接
                                c.finishConnect();
                                // 向服务器发送消息
                                sendBuf.clear();
                                sendBuf.put("客户端消息".getBytes());
                                sendBuf.flip();
                                c.write(sendBuf);
                                // 注册读事件
                                c.register(selector, SelectionKey.OP_READ);
                            }
                        } else if (key.isReadable() && key.isValid()) {
                            // 读事件
                            SocketChannel c = (SocketChannel) key.channel();
                            receiveBuf.clear();
                            int len = c.read(receiveBuf);
                            if (len > 0) {
                                System.out.println("收到了: ");
                                String msg = new String(receiveBuf.array(), 0, len);
                                System.out.println(msg);
                            }
                        }

                        iterator.remove();
                    }
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }).start();
    }
}
```
