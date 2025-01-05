# wait 和 sleep 的区别

- sleep 是 Thread 类的静态方法。wait 是 Object 类的实例方法
- 执行 `sleep(超时时间)` 和 `wait(超时时间)` 的线程都可以在超时时间后恢复执行
- wait 方法可以被 notify 方法唤醒
- wait 方法不传超时时间的话只能等待 notify 方法唤醒
- wait 用于在一个已经进入了同步锁的线程内, 让自己暂时让出锁, 以便其他正在等待此锁的线程可以得到锁并运行, 当前线程必须拥有此对象的锁, 才能调用某个对象的 wait 方法能让当前线程阻塞。调用某个对象的 wait 方法后, 会释放此对象的锁。sleep 则没有这个要求, 在 synchronized 中执行 sleep 方法也并不会释放锁
