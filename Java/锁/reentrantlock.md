# ReentrantLock可重入锁

java除了使用关键字synchronized外，还可以使用ReentrantLock实现独占锁的功能。而且ReentrantLock相比synchronized而言功能更加丰富，使用起来更为灵活，也更适合复杂的并发场景。

ReentrantLock和synchronized区别

1. ReentrantLock和synchronized都是独占锁,只允许线程互斥的访问临界区。synchronized加锁和解锁的过程自动进行，易于操作，但不够灵活。ReentrantLock加锁和解锁的过程需要手动进行，不易操作，但非常灵活。
2. ReentrantLock和synchronized都是可重入的。synchronized因为可重入因此可以放在被递归执行的方法上,且不用担心线程最后能否正确释放锁；而ReentrantLock在重入时要却确保重复获取锁的次数必须和重复释放锁的次数一样，否则可能导致其他线程无法获得该锁。
3. synchronized不可响应中断，一个线程获取不到锁就一直等着；ReentrantLock提供了一个可以响应中断的获取锁的方法lockInterruptibly()。该方法可以用来解决死锁问题。
4. ReentrantLock还可以实现公平锁机制。就是在锁上等待时间最长的线程将获得锁的使用权。

# 使用

```java
// 默认非公平锁
Lock lock = new ReentrantLock();
// 公平锁
// ReentrantLock lock = new ReentrantLock(true);
lock.lock();
try {
 // 处理逻辑
} finally {
    lock.unlock();
}
```
