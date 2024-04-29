# Redisson

是使用 Redisson 分布式锁的基本步骤：

### 1. 添加 Redisson 依赖

```xml
<dependency>
    <groupId>org.redisson</groupId>
    <artifactId>redisson-spring-boot-starter</artifactId>
    <version>3.15.1</version>
</dependency>
```

### 2. 配置 Redisson

通过 `application.yml` 文件配置 Redisson 连接：

```yaml
spring:
  redisson:
    address: "redis://localhost:6379"
```

### 3. 使用 RedissonLock

```java
public class MyService {

    @Autowired
    private RedissonClient redissonClient;

    public void myMethod() {
        RLock lock = redissonClient.getLock("myLock");
        try {
            // 尝试获取锁，最多等待时间10s，以及锁的自动过期时间30s
            if (lock.tryLock(10, 30, TimeUnit.SECONDS)) {
                System.out.println("获取锁成功，执行业务逻辑...");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            // 解锁
            lock.unlock();
        }
    }
}
```

### 4. 自动续期锁

只要锁被持有，并且相关的操作没有完成, Redisson 就会自动续期分布式锁的过期时间，。

## watchdog 机制

Redisson 的 Watchdog 是 Redisson 分布式锁功能的一个特性，它用于确保分布式锁的安全性，特别是在处理网络问题或应用崩溃时，避免出现锁无法释放导致的死锁情况。

Redisson Watchdog 的核心功能是自动续期（auto-renewal）机制。当一个客户端成功获取到锁时，Redisson 会启动一个后台线程，定时发送心跳信号给 Redis，以续期锁的过期时间。这样，只要客户端还在正常运行，锁就不会过期。这个后台线程通常被称为 Watchdog 线程。它的任务是在锁持有期间，周期性地更新锁的过期时间，通常是锁原始过期时间的一小部分。如果客户端在执行任务时突然崩溃或与 Redis 通信失败，Watchdog 线程将无法继续发送心跳信号。在锁超时后，Redisson 会在 Redis 中检查是否存在一个过期的锁。如果是，Redisson 会认为锁的持有者已经失效，并自动释放该锁。

注意: 在调用 tryLock 方法时, 如果设置了锁的自动过期时间, 就不会启动 watchdog 机制了。

## 可重入锁

Redisson 提供的锁是可重入的。可重入锁意味着同一个线程可以多次获取同一把锁，而不会触发死锁。线程必须释放相同数量的锁次数才能完全释放锁。

在 Redisson 中，当使用 `RLock` 接口获取锁时，可以多次对同一个锁调用 `lock()` 方法，而不会阻塞。Redisson 内部会跟踪同一个线程获取锁的次数，并确保只有在锁被完全释放指定次数后，其他线程才能获取到这把锁。

以下是使用 Redisson 可重入锁的示例：

```java
public class LockService {

    @Autowired
    private RedissonClient redissonClient;

    public void performAction() {
        RLock lock = redissonClient.getLock("myLock");

        // 第一次获取锁
        lock.lock();
        try {
            // 执行一些操作
            doSomething();

            // 第二次获取同一把锁（可重入）
            lock.lock();
            try {
                // 执行更多操作
                doAnotherThing();
            } finally {
                // 释放锁一次，因为锁被获取了两次
                lock.unlock();
            }
        } finally {
            // 释放锁
            lock.unlock();
        }
    }
}
```

Redisson 的可重入锁（Reentrant Lock）原理基于 Redis 的原子命令，以及 Redisson 客户端内部的线程安全和计数机制。以下是 Redisson 实现可重入锁的核心原理：

1. **线程标识**：Redisson 为每个线程生成一个唯一的标识（通常是线程的 ID）。

2. **锁的获取**：当一个线程第一次尝试获取锁时，Redisson 使用 Redis 的原子命令（如 `SET` 命令结合 `NX` 和 `PX` 选项）来设置一个锁键（lock key），并关联这个线程的标识。

3. **锁的计数器**：Redisson 内部为每个锁维护一个计数器（lock count）。当线程成功获取锁时，这个计数器会递增。

4. **可重入**：如果同一个线程再次尝试获取已经持有的锁，Redisson 会识别线程标识，并增加锁的计数器，而不是阻塞或失败。

5. **锁的释放**：只有当锁的计数器达到零（即线程释放了与获取次数相同数量的锁）时，锁才会真正被释放。这确保了锁的正确释放，即使在重入的情况下。

6. **公平性**：Redisson 还支持公平锁，这意味着锁的获取顺序将按照请求的顺序进行，而不管线程是否能够立即获取锁。

7. **锁超时**：Redisson 通过在锁键上设置一个超时时间（使用 `PX` 选项）来避免死锁。即使持有锁的线程崩溃，锁也会在超时后自动释放。

8. **锁续期**：Redisson 的 Watchdog 机制会监控锁的超时时间，并在锁即将过期时自动续期，只要持有锁的线程仍然存活。

9. **锁释放的安全性**：Redisson 使用 Lua 脚本来安全地释放锁，Lua 脚本能够原子性地检查并确保只有持有锁的线程才能减少锁的计数器并释放锁。

## RedLock

在单个节点的 Redis 中, 假如 Redis 节点宕机了，那么所有客户端就都无法获得锁了，服务变得不可用。为了提高可用性，可以给这个 Redis 节点增加一个从节点，当主节点不可用的时候，系统自动切到从节点上。但由于 Redis 的主从复制是异步的，这可能导致在 切换节点的过程中丧失锁的安全性。比如:

1. 客户端 1 从 Master 获取了锁
2. Master 宕机了，存储锁的 key 还没有来得及同步到 Slave 上
3. Slave 升级为 Master
4. 客户端 2 从新的 Master 获取到了对应同一个资源的锁
5. 于是，客户端 1 和客户端 2 同时持有了同一个资源的锁

RedLock 算法的核心思想是，通过在多个独立的 Redis 主节点上获取和释放锁来减少单点故障的风险。Redlock 需要部署 N 个独立的 Redis 主节点，且实例之间没有任何的联系。使用独立实例是为了避免 Redis 主从异步复制导致锁丢失。

### RedLock 算法的基本步骤

1. **获取当前时间**：客户端获取当前时间戳，用于后续计算锁的超时时间。

2. **尝试获取锁**：客户端按顺序尝试从 N 个独立的 Redis 主节点获取锁。每个 Redis 节点的锁是一个独立的资源，客户端尝试使用 `SET` 命令带有 `NX` 和 `PX` 选项来设置锁。

3. **计算获取锁的总时间**：客户端计算从第一个 Redis 节点获取锁的时间到最后一个节点的时间差。

4. **锁的有效性检查**：如果客户端在 `lock_timeout / 2` 的时间内（即小于锁超时时间的一半）从大多数（大于 N/2）的 Redis 节点成功获取了锁，那么锁就是有效的。

5. **锁的续期**：客户端定期续期锁，只要锁还在，就通过发送一个 Lua 脚本来更新锁的超时时间。

6. **释放锁**：当锁不再需要时，客户端通过发送 Lua 脚本来释放所有 Redis 节点上的锁, 不管这些节点当时在获取锁的时候成功与否。

Redisson 实现 RedLock：

```java
public class RedisLockService {

    @Autowired
    private RedissonClient redissonClient;

    public void performAction() {
        // 获取 RedLock 实例
        RedLock redLock = redissonClient.getRedLock("myLock");

        try {
            // 尝试获取锁，设置锁的超时时间和锁定尝试时间
            if (redLock.tryLock(10, 30, TimeUnit.SECONDS)) {
                System.out.println("获取锁成功，执行业务逻辑...");
            }
        } finally {
            // 释放锁
            redLock.unlock();
        }
    }
}
```

### 缺点

RedLock 算法作为一种实现分布式锁的机制，虽然提高了锁的可靠性，但它也有一些缺点和局限性：

1. **复杂性**：RedLock 算法比单个 Redis 实例上的锁更复杂，它需要运行和维护多个独立的 Redis 主节点。

2. **资源消耗**：为了实现 RedLock，你可能需要更多的硬件资源，因为需要多个独立的 Redis 实例。

3. **主从复制**：RedLock 要求 Redis 节点之间不能有主从复制，这限制了系统的可用性，因为主从复制是提高 Redis 性能和数据安全性的常用手段。

4. **哨兵兼容性**：RedLock 与 Redis 哨兵（Sentinel）不兼容，因为哨兵会尝试在 Redis 主节点故障时进行自动故障转移，这可能会影响 RedLock 的锁机制。

5. **时钟漂移**：RedLock 依赖于准确的时钟，如果 Redis 节点之间的时钟有漂移，可能会导致锁提前过期或锁的续期失败。

6. **性能问题**：由于需要与多个 Redis 节点通信，RedLock 可能比单个实例的锁有更高的延迟。

7. **容错性**：即使使用了 RedLock，系统仍然需要处理那些极少数情况下的锁失效问题，例如，持有锁的客户端在执行操作期间崩溃，而锁尚未释放。

   - 假设一共有 5 个 Redis 节点：A, B, C, D, E。设想发生了如下的事件序列：
     1. 客户端 1 成功锁住了 A, B, C，获取锁成功（但 D 和 E 没有锁住）。
     2. 节点 C 崩溃重启了，但客户端 1 在 C 上加的锁没有持久化下来，丢失了。
     3. 节点 C 重启后，客户端 2 锁住了 C, D, E，获取锁成功。
