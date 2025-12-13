# 实现一个简单的聊天室

```java
package com.example;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.util.Iterator;
import java.util.Map;
import java.util.HashMap;

public class NioChatServer {

    private Selector selector;
    // 记录每个客户端的一些信息，这里只简单的记录客户端的名字
    private final Map<SocketChannel, String> clientNames = new HashMap<>();

    /**
     * 启动服务
     *
     * @param port 端口
     */
    public void start(int port) throws IOException {
        // 1. 打开 Selector
        selector = Selector.open();

        // 2. 打开 ServerSocketChannel
        ServerSocketChannel serverChannel = ServerSocketChannel.open();
        serverChannel.configureBlocking(false);
        serverChannel.bind(new InetSocketAddress(port));

        // 3. 注册到 Selector，关注 ACCEPT 事件
        serverChannel.register(selector, SelectionKey.OP_ACCEPT);

        System.out.println("NIO Chat Server started at port " + port);

        // 4. 主循环
        while (true) {
            // 阻塞等待事件
            selector.select();

            // 拿到就绪的 key 集合
            Iterator<SelectionKey> keyIterator = selector.selectedKeys().iterator();

            while (keyIterator.hasNext()) {
                SelectionKey key = keyIterator.next();
                keyIterator.remove(); // 必须移除，否则下次还会处理

                try {
                    if (key.isValid() && key.isAcceptable()) {
                        // 有新的客户端连接进来了
                        handleAccept(key);
                    }
                    if (key.isValid() && key.isReadable()) {
                        // 某个客户端发来了数据
                        handleRead(key);
                    }
                } catch (IOException e) {
                    // 某个客户端异常断开
                    handleClientClose(key);
                }
            }
        }
    }

    /**
     * 处理新连接
     */
    private void handleAccept(SelectionKey key) throws IOException {
        ServerSocketChannel ssc = (ServerSocketChannel) key.channel();
        SocketChannel clientChannel = ssc.accept();
        clientChannel.configureBlocking(false);

        // 注册读事件
        clientChannel.register(selector, SelectionKey.OP_READ);

        // 记录客户端
        String clientName = "Client-" + clientChannel.hashCode();
        clientNames.put(clientChannel, clientName);

        System.out.println(clientName + " connected: " + clientChannel.getRemoteAddress());

        // 通知其他人，有新人加入
        broadcast(clientChannel, "[系统] " + clientName + " 加入聊天室\n");
        // 给新来的客户端发一条欢迎消息
        sendToClient(clientChannel, "[系统] 欢迎你，" + clientName + "！当前在线人数：" + clientNames.size() + "\n");
    }

    /**
     * 处理客户端发来的消息
     */
    private void handleRead(SelectionKey key) throws IOException {
        SocketChannel clientChannel = (SocketChannel) key.channel();
        ByteBuffer buffer = ByteBuffer.allocate(1024);

        int read = clientChannel.read(buffer);
        if (read <= 0) {
            // 客户端断开
            handleClientClose(key);
            return;
        }

        // 由写模式切换到读模式
        buffer.flip();
        byte[] bytes = new byte[buffer.remaining()];
        buffer.get(bytes);
        String msg = new String(bytes).trim();

        String clientName = clientNames.getOrDefault(clientChannel, "Unknown");

        System.out.println(clientName + " 说: " + msg);

        // 如果是退出指令
        if ("quit".equalsIgnoreCase(msg) || "exit".equalsIgnoreCase(msg)) {
            sendToClient(clientChannel, "[系统] 已退出聊天室，再见～\n");
            handleClientClose(key);
            return;
        }

        // 正常消息：广播给其他客户端
        String finalMsg = "[" + clientName + "]: " + msg + "\n";
        broadcast(clientChannel, finalMsg);
    }

    /**
     * 广播消息给除了 sender 以外的所有客户端
     */
    private void broadcast(SocketChannel sender, String msg) {
        ByteBuffer buffer = ByteBuffer.wrap(msg.getBytes());
        for (SocketChannel ch : clientNames.keySet()) {
            if (ch.equals(sender)) {
                continue;
            }
            try {
                buffer.rewind(); // 每次写之前倒回去
                ch.write(buffer);
            } catch (IOException e) {
                // 写失败就当对方掉线了
                closeChannelSilently(ch);
            }
        }
    }

    /**
     * 给单个客户端发消息
     */
    private void sendToClient(SocketChannel client, String msg) {
        try {
            ByteBuffer buffer = ByteBuffer.wrap(msg.getBytes());
            client.write(buffer);
        } catch (IOException e) {
            closeChannelSilently(client);
        }
    }

    /**
     * 处理客户端关闭/异常
     */
    private void handleClientClose(SelectionKey key) {
        SocketChannel clientChannel = (SocketChannel) key.channel();
        String clientName = clientNames.remove(clientChannel);
        if (clientName != null) {
            System.out.println(clientName + " disconnected");
            // 通知其他人离开
            broadcast(clientChannel, "[系统] " + clientName + " 离开聊天室\n");
        }
        closeChannelSilently(clientChannel);
        key.cancel();
    }

    /**
     * 关闭 SocketChannel
     */
    private void closeChannelSilently(SocketChannel ch) {
        try {
            ch.close();
        } catch (IOException ignored) {
        }
    }


    static void main(String[] args) throws IOException {
        NioChatServer chatServer = new NioChatServer();
        chatServer.start(8888);
    }
}
```

## 测试这个聊天室

用多个客户端连接。

窗口 1：

```sh
telnet 127.0.0.1 8888
```

窗口 2：

```sh
telnet 127.0.0.1 8888
```

然后在任意一个窗口输入内容回车，另一个窗口就能看到广播的消息。

想退出某个客户端：输入 quit 或 exit 回车。
