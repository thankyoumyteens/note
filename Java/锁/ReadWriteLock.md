# 读写锁

在Java中通过Lock接口及对象可以方便地为对象加锁和释放锁，但是这种锁不区分读写，叫作普通锁。

为了提高性能，Java提供了读写锁。读写锁分为读锁和写锁两种，多个读锁不互斥、读锁与写锁互斥、写锁与写锁互斥。在读的地方使用读锁，在写的地方使用写锁，在没有写锁的情况下，读是无阻塞的。

如果系统要求共享数据可以同时支持很多线程并发读，但不能支持很多线程并发写，那么使用读锁能很大程度地提高效率；如果系统要求共享数据在同一时刻只能有一个线程在写，且在写的过程中不能读取该共享数据，则需要使用写锁。

一般做法是分别定义一个读锁和一个写锁，在读取共享数据时使用读锁，在使用完成后释放读锁，在写共享数据时使用写锁，在使用完成后释放写锁。

在Java中，通过读写锁的接口java.util.concurrent.locks.ReadWriteLock的实现类ReentrantReadWriteLock来完成对读写锁的定义和使用。

```java
ReentrantReadWriteLock lock = new ReentrantReadWriteLock();
Thread t1 = new Thread(new Runnable() {
    @Override
    public void run() {
        lock.writeLock().lock();
        System.out.println();
        lock.writeLock().unlock();
    }
});
Thread t2 = new Thread(new Runnable() {
    @Override
    public void run() {
        lock.readLock().lock();
        System.out.println();
        lock.readLock().unlock();
    }
});
```
