# synchronized 原理

两个字节码指令:

- monitorenter: 加锁
- monitorexit: 解锁

monitor 结构:

- WaitSet
- EntryList
- Owner

synchronized 执行步骤:

1. 线程 1 来的时候, 会把 Owner 指向当前线程 1
2. 其它线程到来, 会加到 EntryList 中等待
3. 线程 1 释放锁后, EntryList 中的线程开始竞争锁
4. 当持有锁的线程调用 wait 方法后, 会把当前线程加到 WaitSet 中
