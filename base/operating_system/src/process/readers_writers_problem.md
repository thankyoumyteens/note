# 读者-写者问题

读者-写者问题(Readers-Writers Problem)是一个经典的并发控制问题, 用于描述对共享数据的访问冲突。在这个问题中, 有两类用户: 读者(Readers)和写者(Writers)。读者只想读取数据, 而写者则会修改数据。允许多个读者同时读取, 但写者必须独占访问。

要求: 

1. 允许多个读者可以同时对文件执行读操作
2. 只允许一个写者往文件中写信息
3. 任一写者在完成写操作之前不允许其他读者或写者工作
4. 写者执行写操作前, 应让已有的读者和写者全部退出

互斥关系: 

- 写进程 - 写进程
- 写进程 - 读进程
- 读进程与读进程不存在互斥问题

以下是使用信号量解决读者-写者问题的一个简化的伪代码示例: 

```c
// 信号量, 用于记录正在读取的读者数量
semaphore readerCount = 0;
// 互斥锁, 保证readerCount的互斥访问
semaphore readerCountMutex = 1;
// 互斥锁, 用于控制读者和写者的互斥访问
semaphore readWriteMutex = 1;

void reader() {
    while (true) {
        // 进入readerCount的临界区
        P(&readerCountMutex);
        // 增加正在读取的读者数量
        readerCount++;
        // 如果是第一个读者, 需要锁定写者
        if (readerCount == 1) {
            // 锁定写者
            P(&readWriteMutex);
        }
        // 离开临界区
        V(&readerCountMutex);

        // 读取数据
        doRead();

        // 再次进入readerCount的临界区
        P(&readerCountMutex);
        // 减少正在读取的读者数量
        readerCount--;
        // 如果没有读者了, 解锁写者
        if (readerCount == 0) {
            // 解锁写者
            V(&readWriteMutex);
        }
        // 离开临界区
        V(&readerCountMutex);
    }
}

void writer() {
    while (true) {
        // 进入临界区
        P(&readWriteMutex);

        // 写入数据
        doWrite();

        // 离开临界区
        V(&readWriteMutex);
    }
}
```

潜在的问题: 如果一直有读进程还在读, 写进程就要一直阻塞等待, 可能“饿死”。因此, 这种算法中, 读进程是优先的。

改进:

```c
// 信号量, 用于记录正在读取的读者数量
semaphore readerCount = 0;
// 互斥锁, 保证readerCount的互斥访问
semaphore readerCountMutex = 1;
// 互斥锁, 用于控制读者和写者的互斥访问
semaphore readWriteMutex = 1;
// 信号量, 用于避免写者饥饿
semaphore turnstile = 1;

void reader() {
    while (true) {
        // 读者等待, 直到获得许可
        P(&turnstile);
        // 进入readerCount的临界区
        P(&readerCountMutex);
        // 增加正在读取的读者数量
        readerCount++;
        // 如果是第一个读者, 需要锁定写者
        if (readerCount == 1) {
            // 锁定写者
            P(&readWriteMutex);
        }
        // 离开临界区
        V(&readerCountMutex);
        // 下一个读者/写者可以继续
        V(&turnstile);

        // 读取数据
        doRead();

        // 再次进入readerCount的临界区
        P(&readerCountMutex);
        // 减少正在读取的读者数量
        readerCount--;
        // 如果没有读者了, 解锁写者
        if (readerCount == 0) {
            // 解锁写者
            V(&readWriteMutex);
        }
        // 离开临界区
        V(&readerCountMutex);
    }
}

void writer() {
    while (true) {
        // 写者等待, 直到获得许可
        P(&turnstile);
        // 进入临界区
        P(&readWriteMutex);

        // 写入数据
        doWrite();

        // 离开临界区
        V(&readWriteMutex);
        // 下一个读者/写者可以继续
        V(&turnstile);
    }
}
```

这样, 只要有写者获取到 turnstile, 就不会继续增加读者, 等到当前的读者全部退出后, 写者就可以执行了。
