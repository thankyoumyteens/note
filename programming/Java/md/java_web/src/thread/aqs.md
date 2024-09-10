# AQS

AQS，全称为 AbstractQueuedSynchronizer，是 Java 中的一个抽象类，它提供了一种用于构建锁和其他同步器的框架。AQS 是 Java 并发包(java.util.concurrent)的一部分，它使用了一个内部的 FIFO(先进先出)队列来管理线程对共享资源的访问。

AQS 的核心思想是通过一个整数(state)来表示同步状态，并通过内置的 FIFO 队列来管理那些请求资源但无法立即获得资源的线程。当一个线程请求一个已经被占用的资源时，这个线程会被包装为一个节点并加入到队列中，然后线程会被暂时挂起。当资源被释放时，队列中的第一个节点(通常是队列的头部)会被唤醒，以便尝试获取资源。

AQS 是许多 Java 并发工具类的基石，比如 ReentrantLock、CountDownLatch、Semaphore、ReadWriteLock 等，都是基于 AQS 实现的。
