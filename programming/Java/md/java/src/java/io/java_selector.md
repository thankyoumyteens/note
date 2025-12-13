# Selector

Selector 是 Java NIO 中实现多路复用的关键。

NIO 真正厉害的地方在网络 IO，也就是：一个线程可以管理成百上千个连接。 避免线程之间上下文切换带来的开销, 减少多个线程占用的系统资源。

核心类：

- Selector：事件分发中心（谁有数据、谁有连接来了，都在这儿通知）
- ServerSocketChannel：服务端监听端口
- SocketChannel：和每个客户端之间的连接
- SelectionKey：描述一个 channel 在 selector 上的“兴趣事件”和“就绪事件”

使用步骤

1. 启动服务器，创建 Selector
2. 服务端通道（ServerSocketChannel）注册到 Selector，关心 OP_ACCEPT
3. 进入死循环：selector.select() 阻塞等待事件
4. 谁有事件（新连接 / 可读），就返回对应的 SelectionKey
5. 根据 key.isAcceptable() / key.isReadable() 做相应处理
6. 全程只有一个线程在跑，但可以同时管理很多连接
