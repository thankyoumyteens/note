# SocketAPI 重构

Java 13 对 Socket API 的重构 是核心语法与功能优化之一，核心目标是：替换老旧的 java.net.Socket/java.net.ServerSocket 底层实现（基于 PlainSocketImpl），提供更简洁、可维护、易调试的新实现，同时完全兼容原有 API，避免开发者修改代码。

Java 早期的 Socket/ServerSocket 底层依赖 PlainSocketImpl，该实现存在以下问题：

- 代码陈旧冗余：基于 JDK 1.0 设计，大量原生（native）代码与 Java 代码混合，维护成本高
- 同步阻塞设计复杂：依赖 Thread.sleep() 轮询、原生锁等实现超时机制，逻辑晦涩
- 调试困难：原生代码与 Java 代码交叉，排查连接超时、端口占用等问题时缺乏清晰日志
- 扩展性差：难以适配新的网络特性（如 TLS 1.3、UDP 优化），且与 NIO（java.nio.channels）体系割裂

为解决这些问题，Java 13 引入了 新的 Socket 实现（NIO-based），并通过系统属性控制是否启用。

Java 13 的 Socket 重构核心是 用 NIO 框架重写底层实现，而非推翻原有 API。新实现具有以下特点：

- 纯 Java 实现：移除大量 native 代码，全部用 Java 代码实现，依赖 java.nio.channels.SocketChannel/ServerSocketChannel，与 NIO 体系统一
- 简化超时机制：利用 NIO 的 Selector 实现非阻塞超时控制，替代旧实现的 Thread.sleep() 轮询，性能更优、逻辑更清晰
- 更好的可调试性：纯 Java 代码便于打断点、输出日志，支持 JVM 层面的调试工具（如 jstack、jmap）
- 完全兼容原有 API：Socket/ServerSocket 的公开方法（如 connect()、accept()、getInputStream()）完全不变，开发者无需修改代码
- 性能持平或提升：新实现避免了旧实现的原生代码切换开销，在高并发场景下连接建立 / 关闭的效率略有提升
