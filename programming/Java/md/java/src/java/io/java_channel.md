# Channel

NIO 是基于通道(Channel)和缓冲区(Buffer)进行操作, 数据总是从 Channel 读取到 Buffer 中, 或者从 Buffer 写入到 Channel 中。

常见的通道：

- FileChannel：文件读写
- SocketChannel：TCP 客户端
- ServerSocketChannel：TCP 服务器
- DatagramChannel：UDP

特点：

- 通道 + 缓冲区 联合使用
- 通道负责和“外部”打交道（文件、网络），缓冲区负责和“你的代码”打交道
