# SETNX

`SETNX` 是 Redis 命令的一个缩写, 代表 "SET if Not eXists"。这个命令用于设置一个键值对, 但它只在键不存在时才会设置成功。如果键已经存在, `SETNX` 命令将不会执行任何操作。`SETNX` 是一个原子操作, 这意味着它要么完全执行, 要么完全不执行, 不会出现中间状态。

`SETNX` 常用于实现分布式锁或原子操作, 因为它能够确保键的唯一性。在多个客户端竞争资源时, 可以使用 `SETNX` 来确保只有一个客户端能够成功设置键。

### 命令格式: 

```shell
SETNX key value
```

- `key`: 要设置的键。如果 `key` 不存在, `SETNX` 命令将设置 `key` 为 `value`, 并且返回 1, 表示操作成功。如果 `key` 已经存在, 无论其值是什么, `SETNX` 命令将不执行任何操作, 并且返回 0, 表示操作未执行
- `value`: 要设置的值。

`SETNX` 命令在 Redis 2.6.12 版本之后已经被 `SET` 命令的选项所取代, 使用 `SET key value NX` 或 `SET key value NX PX 过期时间` 可以达到相同的效果。

### 使用 SETNX 实现分布式锁

1. **设置锁**: 当一个节点想要获取锁时, 它可以通过向 Redis 设置一个键(如`lock_key`)来实现。这个键的值通常是当前节点的标识符(例如一个 UUID), 并且会设置一个过期时间, 以防止持有锁的节点崩溃而无法释放锁

   ```shell
   SET lock_key uuid NX PX 30000
   ```

   其中, `30000` 是锁的过期时间, `NX` 表示如果 `lock_key` 已经存在, 则不执行设置操作

2. **获取锁**: 如果设置成功, 表示该节点成功获取了锁

3. **执行操作**: 持有锁的节点可以安全地执行操作

4. **释放锁**: 操作完成后, 节点需要释放锁。这通常通过删除键来实现

   ```shell
   DEL lock_key
   ```

5. **锁的续期**: 在某些情况下, 持有锁的节点可能需要执行耗时较长的操作。为了防止在操作完成前锁过期, 节点可以定期延长锁的过期时间

   ```shell
   EXPIRE lock_key 30000
   ```

```java
public class RedisDistributedLock {

    // Redis 服务器地址和端口
    private static final String REDIS_SERVER = "localhost";
    private static final int REDIS_PORT = 6379;

    // 锁的过期时间, 这里设置为 10 秒
    private static final int LOCK_EXPIRE_MS = 10000;
    // 锁续期时间(以毫秒为单位), 不能超过锁超时时间
    private static final int LOCK_RENEWAL_MS = 3000;

    /**
     * 尝试获取锁
     */
    public static boolean tryGetLock(String uuid) {
        Jedis jedis = new Jedis(REDIS_SERVER, REDIS_PORT);
        try {
            // 使用 SET 命令加锁, 并设置过期时间
            String result = jedis.set("lock_key", uuid, "NX", "PX", LOCK_EXPIRE_MS);
            return "OK".equals(result);
        } finally {
            jedis.close();
        }
    }

    /**
     * 释放锁
     */
    public static void releaseLock(String uuid, Thread lockRenewalThread) {
        Jedis jedis = new Jedis(REDIS_SERVER, REDIS_PORT);
        try {
            // 只有持有锁的客户端才能释放锁
            // 使用Lua脚本保证操作原子性
            String script = "if redis.call('get', KEYS[1]) == ARGV[1] then return redis.call('del', KEYS[1]) else return 0 end";
            // KEYS[1] 是锁的键, ARGV[1] 是锁的值(uuid)
            jedis.eval(script, 1, "lock_key", uuid);
        } finally {
            // 锁被成功释放, 中断续期线程
            lockRenewalThread.interrupt();
            jedis.close();
        }
    }

    /**
     * 锁续期
     * 续期操作通常在单独的线程中执行, 这样即使主线程在执行长时间操作, 锁也可以被续期
     */
    public static void renewLockLease() {
        Jedis jedis = new Jedis(REDIS_SERVER, REDIS_PORT);
        try {
            // 循环续期, 直到线程被中断或锁被释放
            while (!Thread.currentThread().isInterrupted()) {
                // 锁续期
                String script = "redis.call('expire', KEYS[1], ARGV[1])";
                jedis.eval(script, 1, "lock_key", String.valueOf(LOCK_EXPIRE_MS / 1000));
                TimeUnit.MILLISECONDS.sleep(LOCK_RENEWAL_MS);
            }
        } catch (InterruptedException e) {
            // 如果线程被中断, 不续期锁
            Thread.currentThread().interrupt();
        } finally {
            jedis.close();
        }
    }

    public static void main(String[] args) throws InterruptedException {
        String uuid = UUID.randomUUID().toString();
        if (tryGetLock(uuid)) {
            try {
                System.out.println("获取锁成功, 执行业务逻辑...");
                // 启动一个新线程来续期锁
                Thread lockRenewalThread = new Thread(RedisDistributedLock::renewLockLease);
                lockRenewalThread.start();

                // 模拟耗时操作
                TimeUnit.SECONDS.sleep(5);
            } finally {
                // 释放锁
                releaseLock(uuid, lockRenewalThread);
                // 等待续期线程结束
                Thread lockRenewalThread.join();
            }
        } else {
            System.out.println("获取锁失败...");
        }
    }
}
```
