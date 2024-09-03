# 关键字 volatile

关键字 volatile 是 JVM 提供的最轻量级的同步机制。

当一个变量被定义成 volatile 之后, 它将具备两项特性:

1. 保证此变量对所有线程的可见性
2. 禁止指令重排序优化

## volatile 变量的可见性

可见性是指当一个线程修改了这个变量的值, 新值对于其他线程来说是可以立即得知的。而普通变量并不能做到这一点, 普通变量的值在线程间传递时均需要通过主内存来完成。比如, 线程 A 修改一个普通变量的值, 然后向主内存进行回写, 另外一条线程 B 在线程 A 回写完成了之后再对主内存进行读取操作, 新变量值才会对线程 B 可见。

volatile 变量的可见性保证了当一个线程修改了 volatile 变量的值时, 其他线程可以立即看到这个修改。这是因为 volatile 变量的写操作会立即刷新到主内存, 并且读操作会从主内存中获取最新的值。但是, volatile 并不能保证复合操作的原子性。

如果多个线程同时对 volatile 变量进行复合操作, 例如 i++, 这种操作实际上是由读取、计算和写入三个步骤组成的。由于这是一个复合操作, volatile 不能保证操作的原子性。

由于 volatile 变量只能保证可见性, 在不符合以下两条规则的运算场景中, 仍然要通过加锁来保证原子性:

- 运算结果并不依赖变量的当前值, 或者能够确保只有单一的线程修改变量的值
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

MESI 协议是弱一致性, 由于使用了 store buffer, 不能保证一个线程修改变量后, 其他线程立马可见, 也就是说虽然其他 CPU 状态已经置为无效, 但是当前 CPU 可能将数据修改之后又去做其他事情, 没有来得及将修改后的变量刷新回内存, 而如果此时其他 CPU 需要使用该变量, 则又会从内存中读取到旧的值。JVM 会保证 volatile 变量修改后会立即刷新回内存, 修改操作和写回操作必须是一个原子操作。

## 指令重排序

指令重排序(Instruction Reordering)是编译器和处理器为了提高程序执行效率而进行的一种优化技术。它指的是在不改变单线程程序执行结果的前提下, 重新安排指令的执行顺序。

基础的懒汉式单例模式, 在多线程环境下, 可能会出现多个实例:

```java
public class SingletonObj {
    private static SingletonObj singleton = null;

    private SingletonObj() {}

    public static SingletonObj getInstance() {
        // 用到时才开始创建对象
        if (singleton == null) {
            singleton = new SingletonObj();
        }
        return singleton;
    }
}
```

如果给方法 getInstance()加一个 synchronized 关键字, 虽然可以保证线程安全, 但是这样会导致性能极差。一个优化的方案是在创建对象时使用 synchronized, 而不是加到方法上:

```java
// 通过双重检查锁DCL(double checked locking)的机制实现单例
public class SingletonObj {
    private static SingletonObj singleton = null;

    private SingletonObj() {}

    public static SingletonObj getInstance() {
        if (singleton == null) {
            synchronized (SingletonObj.class) {
                // 可能会被其他线程抢先进入synchronized创建对象
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

这种方式也存在问题, 问题出现在创建对象的语句 singleton = new SingletonObj()上。

编译后的字节码如下:

```
 0: getstatic     #7                  // Field singleton:Lorg/example/normal/SingletonObj;
 3: ifnonnull     37
 6: ldc           #8                  // class org/example/normal/SingletonObj
 8: dup
 9: astore_0
10: monitorenter
11: getstatic     #7                  // Field singleton:Lorg/example/normal/SingletonObj;
14: ifnonnull     27
17: new           #8                  // class org/example/normal/SingletonObj
20: dup
21: invokespecial #13                 // Method "<init>":()V
24: putstatic     #7                  // Field singleton:Lorg/example/normal/SingletonObj;
27: aload_0
28: monitorexit
29: goto          37
32: astore_1
33: aload_0
34: monitorexit
35: aload_1
36: athrow
37: getstatic     #7                  // Field singleton:Lorg/example/normal/SingletonObj;
40: areturn
```

Java 创建对象的操作分为 3 步, 而且不具有原子性:

1. new: 分配内存空间
2. dup: 在栈操作数顶复制一个对象引用给 invokespecial 使用消耗
3. invokespecial 调用`<init>()`方法初始化对象
4. putstatic: 将对象引用赋值给对应的字段

在指令重排序之后的执行顺序可能是这样的:

1. new: 分配内存空间
2. dup: 在栈操作数顶复制一个对象引用给 invokespecial 使用消耗
3. putstatic: 将对象引用赋值给对应的字段
4. invokespecial 调用`<init>()`方法初始化对象

如果有 3 个线程并发使用这个单例对象:

| CPU 时间片 | 线程 A                           | 线程 B                                                             | 线程 C                                                             |
| ---------- | -------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| t1         | 第一次判断 singleton 是否为 null | -                                                                  | -                                                                  |
| t2         | singleton 为 null, 加锁          | -                                                                  | -                                                                  |
| t3         | 第二次判断 singleton 是否为 null | -                                                                  | -                                                                  |
| t4         | -                                | -                                                                  | 第一次判断 singleton 是否为 null                                   |
| t5         | -                                | -                                                                  | singleton 为 null, 加锁, 锁在线程 A 手里, 加锁失败, 开始阻塞等待锁 |
| t6         | singleton 为 null, 开始创建对象  | -                                                                  | -                                                                  |
| t7         | 为对象分配内存空间               | -                                                                  | -                                                                  |
| t8         | 将对象引用赋值给 singleton 变量  | -                                                                  | -                                                                  |
| t9         | -                                | 第一次判断 singleton 是否为 null                                   | -                                                                  |
| t10        | -                                | singleton 不为 null, 访问 singleton 指向的对象(未初始化完成的对象) | -                                                                  |
| t11        | 调用`<init>()`方法初始化对象     | -                                                                  | -                                                                  |
| t12        | 释放锁                           | -                                                                  | -                                                                  |
| t13        | -                                | -                                                                  | 获取到锁, 继续执行                                                 |
| t14        | -                                | -                                                                  | 第二次判断 singleton 是否为 null                                   |
| t15        | -                                | -                                                                  | singleton 不为 null, 访问 singleton 指向的对象                     |

按照这样的顺序执行, 线程 B 将会获得一个未初始化的对象。

## 禁止指令重排序

volatile 关键字则具有禁止指令重排序的特性, 可以保证 volatile 变量的读写操作按照程序的顺序执行。

把 singleton 变量设置成 volatile, 就可以禁止指令重排序, 把 Java 创建对象 3 步固定为下面的顺序:

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
            synchronized (SingletonObj.class) {
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

内存屏障是 CPU 或编译器在对内存随机访问的操作中的一个同步点, 使得此点之前的所有读写操作都执行后才可以开始执行此点之后的操作。它能防止屏障之前的操作与屏障之后的操作交换执行顺序。比如把一个内存屏障插入到两个读操作之间, 那这两个读操作的相对顺序就不会被改变了, 后面的读绝不会先于前面的读执行。

内存屏障可以分为以下几种类型:

1. LoadLoad 屏障: 对于这样的语句 Load1; LoadLoad; Load2, 在 Load2 及后续读取操作要读取的数据被访问前, 保证 Load1 要读取的数据被读取完毕, 并且 Load2 会重新将数据从主内存刷新到工作内存
2. StoreStore 屏障: 对于这样的语句 Store1; StoreStore; Store2, 在 Store2 及后续写入操作执行前, 保证 Store1 的写入操作会强制将数据从工作内存刷新回主内存
3. LoadStore 屏障: 对于这样的语句 Load1; LoadStore; Store2, 在 Store2 及后续写入操作之前, 保证 Load1 要读取的数据被读取完毕, 这条指令只起到禁止重排序的作用, 因为 Load 屏障是加在读操作之前强制从主内存读取数据, Store 屏障加在写操作之后强制将数据写回主内存, 而这里恰好反过来, 所以只起到重排序的作用
4. StoreLoad 屏障: 对于这样的语句 Store1; StoreLoad; Load2, 它的开销是四种屏障中最大的, 它在 Store1 之后会把数据从工作内存刷新回主内存, 也会在 Load2 之前把数据从主内存刷新到工作内存

这些屏障指令并不是真实的 CPU 指令, 他们只是 JMM 定义出来的指令。因为不同硬件实现内存屏障的方式并不相同, JMM 为了屏蔽这种底层硬件平台的不同, 抽象出了这些内存屏障指令, 在运行的时候, 由 JVM 来为不同的平台生成相应的机器码。

为了实现 volatile 的语义, 编译器在生成字节码时, 会在指令序列中插入内存屏障来禁止特定类型的处理器重排序。对于编译器来说, 发现一个最优布置来最小化插入屏障的总数几乎不可能。为此, JMM 采取保守策略:

1. 在每个 volatile 写操作的前面插入一个 StoreStore 屏障
2. 在每个 volatile 写操作的后面插入一个 StoreLoad 屏障
3. 在每个 volatile 读操作的前面插入一个 LoadLoad 屏障
4. 在每个 volatile 读操作的后面插入一个 LoadStore 屏障
