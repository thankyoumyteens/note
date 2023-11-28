# 线程安全

线程安全是指在多线程环境下, 对共享资源的访问和操作不会导致数据的不一致性、不正确性或不可预测的结果。

## 互斥同步

互斥同步(Mutual Exclusion & Synchronization)是一种最常见也是最主要的并发正确性保障手段。同步是指在多个线程并发访问共享数据时, 保证共享数据在同一个时刻只被一条(或者是一些, 当使用信号量的时候)线程使用。而互斥是实现同步的一种手段, 临界区(Critical Section)、互斥量(Mutex)和信号量(Semaphore)都是常见的互斥实现方式。

在 Java 里面, 最基本的互斥同步手段就是 synchronized 关键字, 这是一种块结构(Block Structured)的同步语法。synchronized 关键字经过 Javac 编译之后, 会在同步块的前后分别形成 monitorenter 和 monitorexit 这两个字节码指令。这两个字节码指令都需要一个 reference 类型的参数来指明要锁定和解锁的对象。如果 Java 源码中的 synchronized 明确指定了对象参数, 那就以这个对象的引用作为参数, 如果没有明确指定, 那将根据 synchronized 修饰的方法是实例方法还是类方法, 来决定是取代码所在的对象实例还是取类对应的 Class 对象来作为线程要持有的锁。

在执行 monitorenter 指令时, 首先要去尝试获取对象的锁。如果这个对象没被锁定, 或者当前线程已经持有了那个对象的锁, 就把锁的计数器的值增加一, 而在执行 monitorexit 指令时会将锁计数器的值减一。一旦计数器的值为零, 锁随即就被释放了。如果获取对象锁失败, 那当前线程就应当被阻塞等待, 直到请求锁定的对象被持有它的线程释放为止。

被 synchronized 修饰的同步块对同一条线程来说是可重入的。这意味着同一线程反复进入同步块也不会出现自己把自己锁死的情况。

被 synchronized 修饰的同步块在持有锁的线程执行完毕并释放锁之前, 会无条件地阻塞后面其他线程的进入。这意味着无法像处理某些数据库中的锁那样, 强制已获取锁的线程释放锁, 也无法强制正在等待锁的线程中断等待或超时退出。

持有锁是一个重量级(Heavy-Weight)的操作。Java 的线程是映射到操作系统的原生内核线程之上的, 如果要阻塞或唤醒一条线程, 则需要操作系统来完成, 这就会陷入用户态到核心态的转换中, 进行这种状态转换需要耗费很多的处理器时间。尤其是对于代码特别简单的同步块, 状态转换消耗的时间甚至会比用户代码本身执行的时间还要长。

在 JDK 5 中, Java 类库中新提供了一种全新的互斥同步手段: Lock 接口。重入锁(ReentrantLock)是 Lock 接口最常见的一种实现, 它与 synchronized 一样是可重入的。ReentrantLock 与 synchronized 相比增加了一些高级功能: 

- 等待可中断: 是指当持有锁的线程长期不释放锁的时候, 正在等待的线程可以选择放弃等待, 改为处理其他事情。可中断特性对处理执行时间非常长的同步块很有帮助
- 公平锁: 是指多个线程在等待同一个锁时, 必须按照申请锁的时间顺序来依次获得锁。而非公平锁则不保证这一点, 在锁被释放时, 任何一个等待锁的线程都有机会获得锁。synchronized 中的锁是非公平的, ReentrantLock 在默认情况下也是非公平的, 但可以通过带布尔值的构造函数要求使用公平锁。不过一旦使用了公平锁, 将会导致 ReentrantLock 的性能急剧下降, 会明显影响吞吐量
- 锁绑定多个条件: 是指一个 ReentrantLock 对象可以同时绑定多个 Condition 对象。使用 ReentrantLock 对象的 newCondition()方法可以得到一个 Condition 对象, 可以通过在 Condition 上调用 await()方法来挂起一个线程, 调用 signal()来唤醒一个线程, 调用 signalAll()来唤醒所有在这个 Condition 上被其自身挂起的线程, 这样便可以精确唤醒线程, 而不像 synchronized 那样随便唤醒一个线程或者全部线程

使用 Lock 要确保在 finally 块中释放锁, 否则一旦受同步保护的代码块中抛出异常, 则有可能永远不会释放持有的锁。这一点必须由程序员自己来保证, 而使用 synchronized 的话则可以由 JVM 来确保即使出现异常, 锁也能被自动释放。

## 非阻塞同步

互斥同步面临的主要问题是进行线程阻塞和唤醒所带来的性能开销, 因此这种同步也被称为阻塞同步(Blocking Synchronization)。

互斥同步属于一种悲观的并发策略, 其总是认为只要不去做正确的同步措施, 那就肯定会出现问题, 无论共享的数据是否真的会出现竞争, 它都会进行加锁, 这将会导致用户态到核心态转换、维护锁计数器和检查是否有被阻塞的线程需要被唤醒等开销。

随着硬件指令集的发展, 出现了基于冲突检测的乐观并发策略(乐观并发策略需要操作和冲突检测这两个步骤具备原子性, 这需要硬件指令的支持), 就是不管风险, 先进行操作, 如果没有其他线程争用共享数据, 那操作就直接成功了。如果共享的数据的确被争用, 产生了冲突, 那再进行其他的补偿措施, 最常用的补偿措施是不断地重试, 直到出现没有竞争的共享数据为止。这种乐观并发策略的实现不再需要把线程阻塞挂起, 因此这种同步操作被称为非阻塞同步(Non-Blocking Synchronization), 使用这种措施的代码也常被称为无锁(Lock-Free)编程。

CAS(Compare And Swap, 比较并交换)是一种并发算法, 用于实现多线程环境下的原子操作。CAS 操作是一种乐观锁的实现方式, CAS 指令需要有三个操作数, 分别是内存位置(变量的内存地址, 用 V 表示)、旧的预期值(用 A 表示)和准备设置的新值(用 B 表示)。CAS 指令执行时, 当且仅当 V 符合 A 时, 处理器才会用 B 更新 V 的值, 否则它就不执行更新。但是, 不管是否更新了 V 的值, 都会返回 V 的旧值, 上述的处理过程是一个原子操作, 执行期间不会被其他线程中断。

在 JDK 5 之后, Java 类库中才开始使用 CAS 操作, 该操作由 sun.misc.Unsafe 类里面的 compareAndSwapInt()和 compareAndSwapLong()等几个方法包装提供。这些方法即时编译出来的结果是一条平台相关的处理器 CAS 指令。在 JDK 9 之前只有 Java 类库可以使用 CAS, 而如果用户程序也有使用 CAS 操作的需求, 那要么就采用反射手段突破 Unsafe 的访问限制, 要么就只能通过 Java 类库 API 来间接使用它。直到 JDK 9 之后, Java 类库才在 VarHandle 类里开放了面向用户程序使用的 CAS 操作。

```java
/**
 * Atomic变量自增运算测试
 */
public class AtomicTest {
    public static AtomicInteger race = new AtomicInteger(0);
    public static void increase() {
        // 使用AtomicInteger代替int, 保证了原子性
        race.incrementAndGet();
    }
    private static final int THREADS_COUNT = 20;
    public static void main(String[] args) throws Exception {
        Thread[] threads = new Thread[THREADS_COUNT];
        for (int i = 0; i < THREADS_COUNT; i++) {
            threads[i] = new Thread(new Runnable() {
                @Override
                public void run() {
                    for (int i = 0; i < 10000; i++) {
                        increase();
                    }
                }
            });
            threads[i].start();
        }
        while (Thread.activeCount() > 1)
            Thread.yield();
        System.out.println(race);
    }
}
```

incrementAndGet()方法的 JDK 源码

```java
public final int incrementAndGet() {
    for (;;) {
        int current = get();
        int next = current + 1;
        // CAS操作
        if (compareAndSet(current, next))
            return next;
    }
}
```

incrementAndGet()方法在一个无限循环中, 不断尝试将一个比当前值大一的新值赋值给自己。如果失败了, 那说明在执行 CAS 操作的时候, 旧值已经发生改变, 于是再次循环进行下一次操作, 直到设置成功为止。

CAS 操作存在一个 ABA 问题: 如果一个变量 V 初次读取的时候是 A 值, 并且在准备赋值的时候检查到它仍然为 A 值, 如果在这段期间它的值曾经被改成 B, 后来又被改回为 A, 那 CAS 操作就会误认为它从来没有被改变过。但是大部分情况下 ABA 问题不会影响程序并发的正确性, 如果需要解决 ABA 问题, 改用传统的互斥同步可能会比原子类更为高效。
