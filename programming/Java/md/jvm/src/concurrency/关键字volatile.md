# 关键字volatile

关键字volatile是Java虚拟机提供的最轻量级的同步机制。

当一个变量被定义成volatile之后，它将具备两项特性：

1. 保证此变量对所有线程的可见性
2. 禁止指令重排序优化

# volatile变量的可见性

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

# 禁止指令重排序优化

指令重排序(Instruction Reordering)是编译器和处理器为了提高程序执行效率而进行的一种优化技术。它指的是在不改变程序的语义和结果的前提下，重新安排指令的执行顺序。

普通的变量仅会保证在该方法的执行过程中所有依赖赋值结果的地方都能获取到正确的结果，而不能保证变量赋值操作的顺序与程序代码中的执行顺序一致。而volatile关键字则具有禁止指令重排序的特性，可以保证volatile变量的读写操作按照程序的顺序执行。

```java
// 线程共享变量
Map configOptions;
volatile boolean initialized = false;

// 假设以下代码在线程A中执行
// 模拟读取配置信息，当读取完成后
// 将initialized设置为true,通知其他线程配置可用
void threadA() {
    configOptions = loadFromConfig();
    initialized = true;
}

// 假设以下代码在线程B中执行
// 等待initialized为true，代表线程A已经把配置信息初始化完成
void threadB() {
    while (!initialized) {
        sleep();
    }
    // 使用线程A中初始化好的配置信息
    doSomethingWithConfig();
}
```

如果定义initialized变量时没有使用volatile修饰，就可能会由于指令重排序的优化，导致位于线程A中最后一条代码`initialized=true`被提前执行(重排序优化是机器级的优化操作，提前执行是指这条语句对应的汇编代码被提前执行)，这样在线程B中使用配置信息的代码就可能出现错误，而volatile关键字则可以避免此类情况的发生。

---

假定T表示一个线程，V和W分别表示两个volatile型变量，那么在进行read、load、use、assign、store和write操作时需要满足如下规则：

- 只有当线程T对变量V执行的前一个动作是load的时候，线程T才能对变量V执行use动作。并且，只有当线程T对变量V执行的后一个动作是use的时候，线程T才能对变量V执行load动作。线程T对变量V的use动作可以认为是和线程T对变量V的load、read动作相关联的，必须连续且一起出现。这条规则要求在工作内存中，每次使用V前都必须先从主内存刷新最新的值，用于保证能看见其他线程对变量V所做的修改。
- 只有当线程T对变量V执行的前一个动作是assign的时候，线程T才能对变量V执行store动作。并且，只有当线程T对变量V执行的后一个动作是store的时候，线程T才能对变量V执行assign动作。线程T对变量V的assign动作可以认为是和线程T对变量V的store、write动作相关联的，必须连续且一起出现。这条规则要求在工作内存中，每次修改V后都必须立刻同步回主内存中，用于保证其他线程可以看到自己对变量V所做的修改。
- 假定动作A是线程T对变量V实施的use或assign动作，动作B是线程T对变量W实施的use或assign动作。假定动作P是对变量V的read或write动作，动作Q是对变量W的read或write动作。如果A先于B，那么P先于Q。这条规则要求volatile修饰的变量不会被指令重排序优化，从而保证代码的执行顺序与程序的顺序相同。
