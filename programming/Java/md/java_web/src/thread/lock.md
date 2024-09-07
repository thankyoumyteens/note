# synchronized 和 Lock 的区别

- synchronized 是关键字, 用 C++实现。Lock 是接口, 用 Java 实现
- Lock 提供了 synchronized 没有的特性: 公平锁, 可打断, 可超时, 多条件变量
- Lock 有多个实现适用不同的场景, 如 ReentrantLock, ReentrantReadWriteLock
- 没有竞争时, synchronized 可以使用偏向锁等优化, 性能更好。竞争激烈时, Lock 性能更好
