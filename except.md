# try中有return时finally还会执行吗

try中有return, 会先将值暂存，无论finally语句中对该值做什么处理，最终返回的都是try语句中的暂存值。当try与finally语句中均有return语句，会忽略try中return。

# RabbitMQ六种消息模型

# 消息可靠性投递

# RabbitMQ集群架构模式

# RabbitMQ幂等性

# Redis缓存穿透缓存击穿缓存雪崩

# Redis持久化 AOF RDB

# # Redis哨兵

# Redis数据类型

# Redis缓存过期处理与内存淘汰机制

# Spring中的事务传播行为

# 接口幂等性

# JWT令牌结构

一个JWT由三部分组成：
- Header（头部）: base64编码的Json字符串，Header通常由两部分组成：令牌的类型，即JWT，以及使用的签名算法，例如HMAC SHA256或RSA。
- Payload（载荷） : base64编码的Json字符串，payload是有效载荷，其中包含声明（ claims）。声明包含实体（通常是用户）和其他自定义信息。
- Signature（签名）: 使用指定算法，通过Header和Payload加盐计算的字符串, 保证token在传输的过程中没有被篡改或者损坏

各部分以`.`分割

# JWT工作原理

客户端通过请求将用户名和密码传给服务端，服务端将用户名和密码进行核对，核对成功后将用户id等其他信息作为jwt的有效载荷（payload）与头部进行base64编码形成jwt（字符串），后端将这段字符串作为登陆成功的返回结果返回给前端。前端将其保存在localstroage或sessionstroage里，退出登录时，删除JWT字符串就可以。

每次请求，前端都会把JWT作为authorization请求头传给后端，后端进行检查。

#  == 和 equals 的区别是什么

== 对基本类型是值比较，对引用类型是引用比较。equals 默认情况下是引用比较，只是 String、Integer 等类重写了 equals 方法，把它变成了值比较，所以一般情况下 equals 比较的是值是否相等。

# Math.round(-1.5) 等于多少

等于-1，因为在数轴上取值时是向右取整

# StringBuffer 和 StringBuilder 区别

StringBuffer 是线程安全的，而 StringBuilder 是非线程安全的，但 StringBuilder 的性能却高于 StringBuffer（因为stringbuffer加锁了），所以在单线程环境下推荐使用 StringBuilder，多线程环境下推荐使用 StringBuffer。

# String str="i"与 String str=new String("i")一样吗

不一样，因为内存的分配方式不一样。String str="i"的方式，Java 虚拟机会将其分配到常量池中（常量池保存在方法区中）；而 String str=new String("i") 则会被分到堆内存中。

# 如何将字符串反转？

使用 StringBuilder 或者 stringBuffer 的 reverse() 方法。

或者对撞指针
```java
void reverseString(char[] s) {
    int l = 0;
    int r = s.length - 1;
    while (l < r) {
        swap(s, l++, r--);
    }
}
void swap(char[] arr, int i, int j){
    char t = arr[i];
    arr[i] = arr[j];
    arr[j] = t;
}
```

# BIO、NIO、AIO 有什么区别

- BIO：Block IO 同步阻塞式 IO，就是我们平常使用的传统 IO，它的特点是模式简单使用方便，并发处理能力低。
- NIO：Non IO 同步非阻塞 IO，是传统 IO 的升级，客户端和服务器端通过 Channel（通道）通讯，实现了多路复用。
- AIO：Asynchronous IO 是 NIO 的升级，也叫 NIO2，实现了异步非堵塞 IO ，异步 IO 的操作基于事件和回调机制。

# HashMap 和 Hashtable 有什么区别？

- 存储：HashMap 运行 key 和 value 为 null，而 Hashtable 不允许。
- 线程安全：Hashtable 是线程安全的，而 HashMap 是非线程安全的。
- Hashtable 是保留类不建议使用，推荐在单线程环境下使用 HashMap 替代，多线程使用 ConcurrentHashMap 替代。

# 说一下 HashMap 的实现原理

HashMap 基于 Hash 算法实现的，我们通过 put(key,value)存储，get(key)来获取。当传入 key 时，HashMap 会根据 key. hashCode() 计算出 hash 值，根据 hash 值将 value 保存在 bucket 里。当计算出的 hash 值相同时，我们称之为 hash 冲突，HashMap 的做法是用链表和红黑树存储相同 hash 值的 value。当 hash 冲突的个数比较少时，使用链表否则使用红黑树。

# 说一下 HashSet 的实现原理

HashSet 是基于 HashMap 实现的，HashSet 底层使用 HashMap 来保存所有元素

# ArrayList 和 Vector 的区别是什么？

- 线程安全：Vector 使用了 Synchronized 来实现线程同步，是线程安全的，而 ArrayList 是非线程安全的。
- 性能：ArrayList 在性能方面要优于 Vector。（因为Synchronized）
- 扩容：ArrayList 和 Vector 都会根据实际的需要动态的调整容量，只不过在 Vector 扩容每次会增加 1 倍，而 ArrayList 只会增加 50%。

# 怎么确保一个集合不能被修改

可以使用 Collections. unmodifiableCollection(Collection c) 方法来创建一个只读集合，这样改变集合的任何操作都会抛出 Java. lang. UnsupportedOperationException 异常。

# 并行和并发有什么区别

- 并行：多个处理器或多核处理器同时处理多个任务。
- 并发：多个任务在同一个 CPU 核上，按细分的时间片轮流(交替)执行，从逻辑上来看那些任务是同时执行。

# 创建线程有哪几种方式？

- 继承 Thread 重写 run 方法；
- 实现 Runnable 接口；
- 实现 Callable 接口。

# runnable 和 callable 有什么区别？

runnable 没有返回值，callable 可以拿到返回值和捕获异常

# 线程的5种状态

- 新建(NEW)：新创建了一个线程对象。
- 可运行(RUNNABLE)：线程对象创建后，其他线程调用了该对象的start()方法。该状态的线程位于可运行线程池中，等待被线程调度选中，获取cpu 的使用权 。
- 运行(RUNNING)：可运行状态(runnable)的线程获得了cpu 时间片（timeslice） ，执行程序代码。
- 阻塞(BLOCKED)：阻塞状态是指线程因为某种原因放弃了cpu 使用权，也即让出了cpu timeslice，暂时停止运行。直到线程进入可运行(runnable)状态，才有机会再次获得cpu timeslice 转到运行(running)状态。
- 死亡(DEAD)：线程run()、main() 方法执行结束，或者因异常退出了run()方法，则该线程结束生命周期。死亡的线程不可再次复生。

# sleep() 和 wait() 有什么区别？

- 类的不同：sleep() 来自 Thread，wait() 来自 Object。
- 释放锁：sleep() 不释放锁；wait() 释放锁。
- 用法不同：sleep() 时间到会自动恢复；wait() 可以使用 notify()/notifyAll()直接唤醒。

# notify()和 notifyAll()有什么区别？

notifyAll()会唤醒所有的线程，notify()之后唤醒一个线程。notifyAll() 调用后，会将全部线程由等待池移到锁池，然后参与锁的竞争，竞争成功则继续执行，如果不成功则留在锁池等待锁被释放后再次参与竞争。而 notify()只会唤醒一个线程，具体唤醒哪一个线程由虚拟机控制。

# 创建线程池有哪几种方式？

线程池创建有七种方式，最核心的是最后一种：

- newSingleThreadExecutor()：它的特点在于工作线程数目被限制为 1，操作一个无界的工作队列，所以它保证了所有任务的都是被顺序执行，最多会有一个任务处于活动状态，并且不允许使用者改动线程池实例，因此可以避免其改变线程数目；
- newCachedThreadPool()：它是一种用来处理大量短时间工作任务的线程池，具有几个鲜明特点：它会试图缓存线程并重用，当无缓存线程可用时，就会创建新的工作线程；如果线程闲置的时间超过 60 秒，则被终止并移出缓存；长时间闲置时，这种线程池，不会消耗什么资源。
- newFixedThreadPool(int nThreads)：重用指定数目（nThreads）的线程，其背后使用的是无界的工作队列，任何时候最多有 nThreads 个工作线程是活动的。这意味着，如果任务数量超过了活动队列数目，将在工作队列中等待空闲线程出现；如果有工作线程退出，将会有新的工作线程被创建，以补足指定的数目 nThreads；
- newSingleThreadScheduledExecutor()：创建单线程池，返回 ScheduledExecutorService，可以进行定时或周期性的工作调度；
- newScheduledThreadPool(int corePoolSize)：和newSingleThreadScheduledExecutor()类似，创建的是个 ScheduledExecutorService，可以进行定时或周期性的工作调度，区别在于单一工作线程还是多个工作线程；
- newWorkStealingPool(int parallelism)：这是一个经常被人忽略的线程池，Java 8 才加入这个创建方法，其内部会构建ForkJoinPool，利用Work-Stealing算法，并行地处理任务，不保证处理顺序；
- ThreadPoolExecutor()：是最原始的线程池创建，上面1-3创建方式都是对ThreadPoolExecutor的封装。

# 线程池都有哪些状态？

- RUNNING：这是最正常的状态，接受新的任务，处理等待队列中的任务。
- SHUTDOWN：不接受新的任务提交，但是会继续处理等待队列中的任务。
- STOP：不接受新的任务提交，不再处理等待队列中的任务，中断正在执行任务的线程。
- TIDYING：所有的任务都销毁了，workCount 为 0，线程池的状态在转换为 TIDYING 状态时，会执行钩子方法 terminated()。
- TERMINATED：terminated()方法结束后，线程池的状态就会变成这个。

# 线程池中 submit() 和 execute() 方法有什么区别

- execute()：只能执行 Runnable 类型的任务。
- submit()：可以执行 Runnable 和 Callable 类型的任务。

# synchronized 锁升级的原理

synchronized 锁升级原理：在锁对象的对象头里面有一个 threadid 字段，在第一次访问的时候 threadid 为空，jvm 让其持有偏向锁，并将 threadid 设置为其线程 id，再次进入的时候会先判断 threadid 是否与其线程 id 一致，如果一致则可以直接使用此对象，如果不一致，则升级偏向锁为轻量级锁，通过自旋循环一定次数来获取锁，执行一定次数之后，如果还没有正常获取到要使用的对象，此时就会把锁从轻量级升级为重量级锁。

锁的升级的目的：锁升级是为了减低了锁带来的性能消耗。

- 偏向锁: 指一段同步代码一直被一个线程所访问，那么该线程会自动获取锁，降低获取锁的代价
- 轻量级锁: 当锁是偏向锁的时候，被另外的线程所访问，偏向锁就会升级为轻量级锁，其他线程会通过自旋的形式尝试获取锁，不会阻塞，从而提高性能
- 重量级锁: 因为使用自旋的方式非常消耗CPU，当一定时间内通过自旋的方式无法获取到锁，或者一个线程在持有锁，一个在自旋，又有第三个来访时，轻量级锁升级为重量级锁，此时等待锁的线程都会进入阻塞状态。

自旋: 循环等待，然后不断的判断锁是否能够被成功获取，直到获取到锁才会退出循环

# 什么是死锁

当线程 A 持有独占锁a，并尝试去获取独占锁 b 的同时，线程 B 持有独占锁 b，并尝试获取独占锁 a 的情况下，就会发生 AB 两个线程由于互相持有对方需要的锁，而发生的阻塞现象，我们称为死锁。

# 怎么防止死锁

- 尽量使用 tryLock(long timeout, TimeUnit unit)的方法(ReentrantLock、ReentrantReadWriteLock)，设置超时时间，超时可以退出防止死锁。
- 尽量使用 Java. util. concurrent 并发类代替自己手写锁。
- 尽量降低锁的使用粒度，尽量不要几个功能用同一把锁。
- 尽量减少同步的代码块。

# ThreadLocal 是什么？有哪些使用场景？

ThreadLocal 为每个使用该变量的线程提供独立的变量副本，所以每一个线程都可以独立地改变自己的副本，而不会影响其它线程所对应的副本。

ThreadLocal 的经典使用场景是数据库连接和 session 管理等。

# 说一下 synchronized 底层实现原理？

synchronized 是由一对 monitorenter/monitorexit 指令实现的，synchronized的底层是通过一个monitor的对象来完成。在 Java 6 之前，monitor 的实现完全是依靠操作系统内部的互斥锁，因为需要进行用户态到内核态的切换，所以同步操作是一个无差别的重量级操作，性能也很低。但在 Java 6 的时候，Java 虚拟机 对此进行了大刀阔斧地改进，提供了三种不同的 monitor 实现，也就是常说的三种不同的锁：偏向锁（Biased Locking）、轻量级锁和重量级锁，大大改进了其性能。

每个对象有一个监视器锁（monitor）。当monitor被占用时就会处于锁定状态，线程执行monitorenter指令时尝试获取monitor的所有权，过程如下：

1. 如果monitor的进入数为0，则该线程进入monitor，然后将进入数设置为1，该线程即为monitor的所有者。
2. 如果线程已经占有该monitor，只是重新进入，则进入monitor的进入数加1.
3. 如果其他线程已经占用了monitor，则该线程进入阻塞状态，直到monitor的进入数为0，再重新尝试获取monitor的所有权。

线程执行monitorexit指令时，monitor的进入数减1，如果减1后进入数为0，那线程退出monitor，不再是这个monitor的所有者。其他被这个monitor阻塞的线程可以尝试去获取这个 monitor 的所有权。 

# synchronized 和 volatile 的区别是什么？

- volatile 是变量修饰符；synchronized 是修饰类、方法、代码段。
- volatile 仅能实现变量的修改可见性，不能保证原子性；而 synchronized 则可以保证变量的修改可见性和原子性。
- volatile 不会造成线程的阻塞；synchronized 可能会造成线程的阻塞。

变量的修改可见性: 被volatile关键字修饰的共享变量，如果值发生了变更，其他线程立马可见，避免出现脏读。

Java 内存模型规定所有的共享变量都存储于主内存。每一个线程还存在自己的工作内存，保留了被线程使用的变量的副本。线程对变量的所有的操作都必须在工作内存中完成，而不能直接读写主内存中的变量。不同线程之间也不能直接访问对方工作内存中的变量，线程间变量的值的传递需要通过主内存中转来完成。所以可能会导致线程对共享变量的修改没有即时更新到主内存，从而使得线程在使用共享变量的值时，该值并不是最新的。

当一个线程进入 synchronized 代码块后，线程获取到锁，会清空本地内存，然后从主内存中拷贝共享变量的最新值到本地内存作为副本，执行代码，又将修改后的副本值刷新到主内存中，最后线程释放锁。除了 synchronized 外，其它锁也能保证变量的内存可见性。

使用 volatile 修饰共享变量后，当线程操作变量副本并写回主内存后，会通过 CPU 总线嗅探机制告知其他线程该变量副本已经失效，需要重新从主内存中读取。

# synchronized 和 Lock 有什么区别？

- synchronized 可以给类、方法、代码块加锁；而 lock 只能给代码块加锁。
- synchronized 不需要手动获取锁和释放锁，使用简单，发生异常会自动释放锁，不会造成死锁；而 lock 需要自己加锁和释放锁，如果使用不当没有 unLock()去释放锁就会造成死锁。
- 通过 Lock 可以知道有没有成功获取锁，而 synchronized 却无法办到。

# synchronized 和 ReentrantLock 区别是什么？

- ReentrantLock 使用起来比较灵活，但是必须有释放锁的配合动作；
- ReentrantLock 必须手动获取与释放锁，而 synchronized 不需要手动释放和开启锁；
- ReentrantLock 只适用于代码块锁，而 synchronized 可用于修饰方法、代码块等。

# 说一下 atomic 的原理？

atomic 主要利用 CAS (Compare And Wwap) 和 volatile 和 native 方法来保证原子操作，从而避免 synchronized 的高开销，执行效率大为提升。

# 如何实现对象克隆？

- 实现 Cloneable 接口并重写 Object 类中的 clone() 方法。
- 实现 Serializable 接口，通过对象的序列化和反序列化实现克隆，可以实现真正的深度克隆。

# 深拷贝和浅拷贝区别是什么？

- 浅拷贝：当对象被复制时只复制它本身和其中包含的值类型的成员变量，而引用类型的成员对象并没有复制。
- 深拷贝：除了对象本身被复制外，对象所包含的所有成员变量也将复制。

# session 和 cookie 有什么区别？

- 存储位置不同：session 存储在服务器端；cookie 存储在浏览器端。
- 安全性不同：cookie 安全性一般，在浏览器存储，可以被伪造和修改。
- 容量和个数限制：cookie 有容量限制，每个站点下的 cookie 也有个数限制。
- 存储的多样性：session 可以存储在 Redis 中、数据库中、应用程序中；而 cookie 只能存储在浏览器中。

# 说一下 session 的工作原理？

session 的工作原理是客户端登录完成之后，服务器会创建对应的 session，session 创建完之后，会把 session 的 id 发送给客户端，客户端再存储到浏览器中。这样客户端每次访问服务器时，都会带着 sessionid，服务器拿到 sessionid 之后，在内存找到与之对应的 session 这样就可以正常工作了。

# 如果客户端禁止 cookie 能实现 session 还能用吗？

可以用，session 只是依赖 cookie 存储 sessionid，如果 cookie 被禁用了，可以使用 url 中添加 sessionid 的方式保证 session 能正常使用。

# 如何避免 SQL 注入？

使用预处理 PreparedStatement。
使用正则表达式过滤掉字符中的特殊字符。

# 什么是 XSS 攻击，如何避免？

XSS 攻击：即跨站脚本攻击，它是 Web 程序中常见的漏洞。原理是攻击者往 Web 页面里插入恶意的脚本代码（css 代码、Javascript 代码等），当用户浏览该页面时，嵌入其中的脚本代码会被执行，从而达到恶意攻击用户的目的，如盗取用户 cookie、破坏页面结构、重定向到其他网站等。

预防 XSS 的核心是必须对输入的数据做过滤处理。

# 什么是 CSRF 攻击，如何避免？

CSRF：Cross-Site Request Forgery（中文：跨站请求伪造），可以理解为攻击者盗用了你的身份，以你的名义发送恶意请求。

防御手段：

- 验证请求来源地址；
- 关键操作添加验证码；
- 在请求地址添加 token 并验证。

# 说一下 tcp 粘包是怎么产生的？

tcp 粘包可能发生在发送端或者接收端，分别来看两端各种产生粘包的原因：

- 发送端粘包：发送端需要等缓冲区满才发送出去，造成粘包；
- 接收方粘包：接收方不及时接收缓冲区的包，造成多个包接收。

# OSI 的七层模型都有哪些？

1. 物理层：利用传输介质为数据链路层提供物理连接，实现比特流的透明传输。
1. 数据链路层：负责建立和管理节点间的链路。
1. 网络层：通过路由选择算法，为报文或分组通过通信子网选择最适当的路径。
1. 传输层：向用户提供可靠的端到端的差错和流量控制，保证报文的正确传输。
1. 会话层：向两个实体的表示层提供建立和使用连接的方法。
1. 表示层：处理用户信息的表示问题，如编码、数据格式转换和加密解密等。
1. 应用层：直接向用户提供服务，完成用户希望在网络上完成的各种工作。

# get 和 post 请求有哪些区别？

- get 请求会被浏览器主动缓存，而 post 不会。
- get 传递参数有大小限制，而 post 没有。
- post 参数传输更安全，get 的参数会明文显示在 url 上，post 不会。

# 如何实现跨域？

- 服务器端设置 CORS 等于 *；
- 在单个接口使用注解 @CrossOrigin 运行跨域；
- 使用 jsonp 跨域；

# 说一下 JSONP 实现原理？

利用script标签的 src 连接可以访问不同源的特性，加载远程返回的“JS 函数”来执行的。

# 说一下你熟悉的设计模式？

- 单例模式：保证被创建一次，节省系统开销。
- 工厂模式（简单工厂、抽象工厂）：解耦代码。
- 观察者模式：定义了对象之间的一对多的依赖，这样一来，当一个对象改变时，它的所有的依赖者都会收到通知并自动更新。
- 外观模式：提供一个统一的接口，用来访问子系统中的一群接口，外观定义了一个高层的接口，让子系统更容易使用。
- 模版方法模式：定义了一个算法的骨架，而将一些步骤延迟到子类中，模版方法使得子类可以在不改变算法结构的情况下，重新定义算法的步骤。
- 状态模式：允许对象在内部状态改变时改变它的行为，对象看起来好像修改了它的类。

# 观察者模式

发布者发布信息，订阅者获取信息，订阅了就能收到信息，没订阅就收不到信息。

```java
/**
 * 抽象被观察者接口
 * 声明了添加、删除、通知观察者方法
 */
public interface Observerable {
    void registerObserver(Observer o);
    void removeObserver(Observer o);
    void notifyObserver();
}
/**
 * 抽象观察者
 * 当被观察者调用notifyObserver()方法时，观察者的update()方法会被回调。
 */
public interface Observer {
    public void update(String message);
}
/**
 * 被观察者实现
 */
public class WechatServer implements Observerable {
    
    private List<Observer> list;
    private String message;
    
    public WechatServer() {
        list = new ArrayList<Observer>();
    }
    
    @Override
    public void registerObserver(Observer o) {
        list.add(o);
    }
    
    @Override
    public void removeObserver(Observer o) {
        if(!list.isEmpty())
            list.remove(o);
    }

    @Override
    public void notifyObserver() {
        for(int i = 0; i < list.size(); i++) {
            Observer oserver = list.get(i);
            oserver.update(this.message);
        }
    }
    
    public void setInfomation(String s) {
        this.message = s;
        // 消息更新，通知所有观察者
        notifyObserver();
    }
}
```

# 外观模式

外观模式可以很好地解决让子系统外部的客户端在使用子系统的时候，既能简单地使用这些子系统内部的模块，而又不用客户端去与子系统内部的多个模块交互。

外观模式的目的不是给子系统添加新的功能接口，而是为了让外部减少与子系统内多个模块的交互，松散耦合，从而能让外部更简单的使用子系统。

因为外观是当做子系统对外的接口出现的，虽然也可以定义一些子系统没有的功能，但是不建议这么做。外观应该是包装已有的功能，它主要负责组合已有功能来实现客户需要，而不是添加新的实现。

```java
/**
 * 子系统
 */
public class DrinkableWater {
    public void facadeWater(){
        System.out.println("煮水");
    }
}
/**
 * 子系统
 */
public class Tea {
    public void facadeTea(){
        System.out.println("取茶");
    }
}
/**
 * 子系统
 */
public class TeaCup {
    public void facadeTeaCup(){
        System.out.println("泡茶");
    }
}
/**
 * 外观对象
 */
public class Waiter {
    // 示意方法，满足客户需要的功能
    public void getTea(){
        // 内部实现会调用多个子系统
        DrinkableWater drinkableWater = new DrinkableWater();
        TeaCup teaCup = new TeaCup();
        Tea tea = new Tea();
        tea.facadeTea();
        drinkableWater.facadeWater();
        teaCup.facadeTeaCup(tea);
    }
}
/**
 * 客户端
 */
public class Customer {
    public static void main(String[] args) {
        new Waiter().getTea();
    }
}
```

# 模版方法模式

定义一个操作中的算法的骨架，而将一些步骤延迟到子类中。子类可以置换掉父类的可变部分，但是子类却不可以改变模板方法所代表的顶级逻辑。

```java
// 抽象模板角色类
public abstract class AbstractTemplate {
    // 模板方法, 可以有任意多个
    public void templateMethod(){
        //调用基本方法
        abstractMethod();
        hookMethod();
        concreteMethod();
    }
    // 抽象方法, 由具体子类实现
    protected abstract void abstractMethod();
    // 钩子方法(空方法), 子类可选择实现，不是必须实现
    protected void hookMethod(){}
    // 具体方法, 由抽象类声明并实现，而子类并不实现或置换
    private final void concreteMethod(){
        // ...
    }
}

// 具体模板角色类，实现了父类所声明的基本方法
public class ConcreteTemplate extends AbstractTemplate{
    // 基本方法的实现
    @Override
    public void abstractMethod() {
        // ...
    }
    // 重写父类的方法
    @Override
    public void hookMethod() {
        // ...
    }
}
```

### 应用

Servlet

HttpServlet担任抽象模板角色
- 由service()方法担任模板方法。
- Servlet并非完全按照模板方法定义的那样，而是做了变通，提供了默认doGet、doPost的实现

自己实现的TestServlet担任具体模板角色
- TestServlet置换掉了父类HttpServlet中七个基本方法中的其中两个，分别是doGet和doPost

