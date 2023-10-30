# 关键字volatile

关键字volatile是Java虚拟机提供的最轻量级的同步机制。

当一个变量被定义成volatile之后，它将具备两项特性：

1. 保证此变量对所有线程的可见性
2. 禁止指令重排序优化

## volatile变量的可见性

可见性是指当一条线程修改了这个变量的值，新值对于其他线程来说是可以立即得知的。而普通变量并不能做到这一点，普通变量的值在线程间传递时均需要通过主内存来完成。比如，线程A修改一个普通变量的值，然后向主内存进行回写，另外一条线程B在线程A回写完成了之后再对主内存进行读取操作，新变量值才会对线程B可见。

volatile变量的可见性保证了当一个线程修改了volatile变量的值时，其他线程可以立即看到这个修改。这是因为volatile变量的写操作会立即刷新到主内存，并且读操作会从主内存中获取最新的值。但是，volatile并不能保证复合操作的原子性。

如果多个线程同时对volatile变量进行复合操作，例如i++，这种操作实际上是由读取、计算和写入三个步骤组成的。由于这是一个复合操作，volatile不能保证操作的原子性。

由于volatile变量只能保证可见性，在不符合以下两条规则的运算场景中，仍然要通过加锁来保证原子性：

- 运算结果并不依赖变量的当前值，或者能够确保只有单一的线程修改变量的值
- 变量不需要与其他的状态变量共同参与不变约束

```java
// 适合volatile的使用场景
volatile boolean shutdownRequested;

public void shutdown() {
    shutdownRequested = true;
}

public void doWork() {
    while (!shutdownRequested) {
        // 代码的业务逻辑
    }
}
```

## MESI

MESI协议是弱一致性，由于使用了store buffer，不能保证一个线程修改变量后，其他线程立马可见，也就是说虽然其他CPU状态已经置为无效，但是当前CPU可能将数据修改之后又去做其他事情，没有来得及将修改后的变量刷新回主存，而如果此时其他CPU需要使用该变量，则又会从主存中读取到旧的值。而JVM会保证volatile变量修改后会立即刷新回主存，修改操作和写回操作必须是一个原子操作。

## 指令重排序

指令重排序(Instruction Reordering)是编译器和处理器为了提高程序执行效率而进行的一种优化技术。它指的是在不改变单线程程序执行结果的前提下，重新安排指令的执行顺序。

基础的饱汉式单例模式，在多线程环境下，可能会出现多个实例：

```java
public class SingletonObj {
    private static SingletonObj singleton = null;

    private SingletonObj() {}

    public static SingletonObj getInstance() {
        if (singleton == null) {
            singleton = new SingletonObj();
        }
        return singleton;
    }
}
```

如果给方法getInstance()加一个synchronized关键字，虽然可以保证线程安全，但是这样会导致性能极差。一个优化的方案是在创建对象时使用syncronized，而不是加到方法上：

```java
// 通过双重检查锁DCL(double checked locking)的机制实现单例
public class SingletonObj {
    private static SingletonObj singleton = null;

    private SingletonObj() {}

    public static SingletonObj getInstance() {
        if (singleton == null) {
            syncronized (SingletonObj.class) {
                // 可能会被其他线程抢先进入syncronized创建对象
                // 所以需要再判断一次
                if (singleton == null) {
                    singleton = new SingletonObj();
                }
            }
        }
        return singleton;
    }
}
```

这种方式也存在问题，问题出现在创建对象的语句singleton = new SingletonObj()上。Java创建对象的操作分为3步，而且不具有原子性：

1. 分配内存空间
2. 调用`<init>()`方法初始化对象
3. 将对象内存空间的地址赋值给对应的引用类型变量

在指令重排序之后的执行顺序可能是这样的：

1. 分配内存空间
2. 将对象内存空间的地址赋值给对应的引用类型变量
3. 调用`<init>()`方法初始化对象

CPU时间片 | 线程A | 线程B | 线程C
--|--|--|--
t1 | 第一次判断singleton是否为null | - | -
t2 | singleton为null，加锁 | - | -
t3 | 第二次判断singleton是否为null | - | -
t4 | - | - | 第一次判断singleton是否为null
t5 | - | - | singleton为null，加锁，加锁失败，开始阻塞等待锁
t6 | singleton为null，开始创建对象 | - | -
t7 | 为对象分配内存空间 | - | -
t8 | 将对象内存空间的地址赋值给singleton变量 | - | -
t9 | - | 第一次判断singleton是否为null | -
t10 | - | singleton不为null，访问singleton指向的对象 | -
t11 | 调用`<init>()`方法初始化对象 | - | -
t12 | 释放锁 | - | -
t13 | - | - | 获取到锁，继续执行
t14 | - | - | 第二次判断singleton是否为null
t15 | - | - | singleton不为null，访问singleton指向的对象

按照这样的顺序执行，线程B将会获得一个未初始化的对象。

## 禁止指令重排序

普通的变量仅会保证在该方法的执行过程中所有依赖赋值结果的地方都能获取到正确的结果，而不能保证变量赋值操作的顺序与程序代码中的执行顺序一致。而volatile关键字则具有禁止指令重排序的特性，可以保证volatile变量的读写操作按照程序的顺序执行。

把singleton变量设置成volatile，就可以禁止指令重排序，把Java创建对象3步固定为下面的顺序：

1. 分配内存空间
2. 调用`<init>()`方法初始化对象
3. 将对象内存空间的地址赋值给对应的引用类型变量

```java
public class SingletonObj {
    // 禁止指令重排序
    private static volatile SingletonObj singleton = null;

    private SingletonObj() {}

    public static SingletonObj getInstance() {
        if (singleton == null) {
            syncronized (SingletonObj.class) {
                if (singleton == null) {
                    singleton = new SingletonObj();
                }
            }
        }
        return singleton;
    }
}
```

## 内存屏障

内存屏障是CPU或编译器在对内存随机访问的操作中的一个同步点，使得此点之前的所有读写操作都执行后才可以开始执行此点之后的操作。它能防止屏障之前的操作与屏障之后的操作交换执行顺序。比如把一个内存屏障插入到两个读操作之间，那这两个读操作的相对顺序就不会被改变了，后面的读绝不会先于前面的读执行。

内存屏障可以分为以下几种类型：

1. LoadLoad屏障：对于这样的语句Load1; LoadLoad; Load2，在Load2及后续读取操作要读取的数据被访问前，保证Load1要读取的数据被读取完毕，并且Load2会重新将数据从主内存刷新到工作内存
2. StoreStore屏障：对于这样的语句Store1; StoreStore; Store2，在Store2及后续写入操作执行前，保证Store1的写入操作会强制将数据从工作内存刷新回主内存
3. LoadStore屏障：对于这样的语句Load1; LoadStore; Store2，在Store2及后续写入操作被刷出前，保证Load1要读取的数据被读取完毕，这条指令只起到禁止重排序的作用，因为Load屏障是加在读操作之前强制从主内存读取数据，Store屏障加在写操作之后强制将数据写回主内存，而这里恰好反过来，所以只起到重排序的作用
4. StoreLoad屏障：对于这样的语句Store1; StoreLoad; Load2，在Load2及后续所有读取操作执行前，保证Store1的写入操作会强制将数据从工作内存刷新回主内存。它的开销是四种屏障中最大的，他会把据从工作内存刷新回主内存，也会把数据从主内存刷新到工作内存

这些屏障指令并不是处理器真实的CPU指令，他们只是JMM定义出来的指令。因为不同硬件实现内存屏障的方式并不相同，JMM为了屏蔽这种底层硬件平台的不同，抽象出了这些内存屏障指令，在运行的时候，由JVM来为不同的平台生成相应的机器码。

为了实现volatile的语义，编译器在生成字节码时，会在指令序列中插入内存屏障来禁止特定类型的处理器重排序。对于编译器来说，发现一个最优布置来最小化插入屏障的总数几乎不可能。为此，JMM采取保守策略：

1. 在每个volatile写操作的前面插入一个StoreStore屏障
2. 在每个volatile写操作的后面插入一个StoreLoad屏障
3. 在每个volatile读操作的前面插入一个LoadLoad屏障
4. 在每个volatile读操作的后面插入一个LoadStore屏障
