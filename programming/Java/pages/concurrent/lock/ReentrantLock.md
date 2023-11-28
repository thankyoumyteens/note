# ReentrantLock可重入锁

ReentrantLock继承了Lock接口并实现了在接口中定义的方法, 是一个可重入的独占锁。ReentrantLock通过AQS来实现锁的获取与释放。

ReentrantLock有显式的操作过程, 何时加锁、何时释放锁都在程序员的控制之下。具体的使用流程是定义一个ReentrantLock, 在需要加锁的地方通过lock方法加锁, 等资源使用完成后再通过unlock方法释放锁。

# 使用

```java
// 默认非公平锁
Lock lock = new ReentrantLock();
// 公平锁
// Lock lock = new ReentrantLock(true);
lock.lock();
try {
 // 处理逻辑
} finally {
    lock.unlock();
}
```

# ReentrantLock可重入锁

ReentrantLock锁可以反复进入。即允许连续两次获得同一把锁, 两次释放同一把锁。

```java
Lock lock = new ReentrantLock();
lock.lock();
lock.lock();
try {
 // 处理逻辑
} finally {
    // 获取锁和释放锁的次数要相同
    lock.unlock();
    lock.unlock();
}
```

# 定时锁

当前线程获取锁的时间超过了指定的等待时间, 则将返回false。

```java
boolean tryLock(long time,TimeUnit unit) throws InterruptedException
```

# 公平锁与非公平锁

ReentrantLock通过在构造函数ReentrantLock(boolean fair)中传递不同的参数来定义不同类型的锁, 默认的实现是非公平锁。这是因为, 非公平锁虽然放弃了锁的公平性, 但是执行效率明显高于公平锁。如果系统没有特殊的要求, 一般情况下建议使用非公平锁。
