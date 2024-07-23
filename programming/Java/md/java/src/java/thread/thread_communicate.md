# 线程通信

线程间通信的模型有两种: 共享内存和消息传递, 以下方式都是基本这两种模型来实现的。

线程通信的方法:

1. synchronized 临界区
2. ReentrantLock/Condition 消息队列
3. CountDownLatch
4. LockSupport
5. Socket
6. 信号量机制 Semaphore
7. 管道通信
