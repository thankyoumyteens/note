# Java NIO

NIO 是一整套面向"缓冲区 + 通道 + 选择器"的 API，用来做高性能 IO（文件、网络）。

## NIO 和传统 IO 的区别

| 对比项                  | 传统 IO（java.io）                   | NIO（java.nio）                                |
| ----------------------- | ------------------------------------ | ---------------------------------------------- |
| 编程模型                | 面向流（Stream Oriented）            | 面向缓冲区（Buffer Oriented）                  |
| 阻塞/非阻塞             | 基本都是阻塞                         | 支持非阻塞（Non-blocking）                     |
| 单连接并发模型          | 一连接几乎对应一线程                 | 一个线程可管理成百上千连接（通过 Selector）    |
| 核心对象                | InputStream / OutputStream / Reader… | Channel / Buffer / Selector                    |
| 适用场景                | 简单 IO、小并发                      | 高并发网络、文件传输、大量连接                 |
| API 包                  | `java.io.*` / `java.net.*`           | `java.nio.*` / `java.nio.channels.*` 等        |
| 多路复用（多路复用 IO） | 不支持                               | 支持 Selector（类似 select/poll/epoll 的模式） |
