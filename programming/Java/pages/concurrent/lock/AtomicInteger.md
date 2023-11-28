# AtomicInteger

在多线程程序中, 诸如++i或i++等运算不具有原子性, 因此不是安全的线程操作。可以通过synchronized或ReentrantLock将该操作变成一个原子操作, 但是synchronized和ReentrantLock均属于重量级锁。因此JVM为此类原子操作提供了一些原子操作同步类, 使得同步操作（线程安全操作）更加方便、高效。

AtomicInteger为提供原子操作的Integer的类, 常见的原子操作类还有AtomicBoolean、AtomicInteger、AtomicLong、AtomicReference等, 它们的实现原理相同, 区别在于运算对象的类型不同。还可以通过`AtomicReference<V>`将一个对象的所有操作都转化成原子操作。AtomicInteger的性能通常是synchronized和ReentrantLock的好几倍。

```java
AtomicInteger ai = new AtomicInteger(0); 
System.out.println(ai.addAndGet(1)); //1
System.out.println(ai.getAndAdd(1)); //1 
System.out.println(ai.get()); //2
```
