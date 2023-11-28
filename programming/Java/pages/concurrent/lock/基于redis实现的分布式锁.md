# 基于redis实现的分布式锁

## 加锁

加锁实际上就是在redis中, 给Key键设置一个值, 为避免死锁, 并给定一个过期时间。
```
SET lock_key random_value NX PX 5000
```

- random_value 是客户端生成的唯一的字符串。
- NX 代表只在键不存在时, 才对键进行设置操作。
- PX 5000 设置键的过期时间为5000毫秒。

如果上面的命令执行成功, 则证明客户端获取到了锁。

## 解锁

解锁的过程就是将Key键删除。为了保证解锁操作的原子性, 我们用LUA脚本完成这一操作。先判断当前锁的字符串是否与传入的值相等, 是的话就删除Key, 解锁成功。
```lua
if redis.call('get',KEYS[1]) == ARGV[1] then 
   return redis.call('del',KEYS[1]) 
else
   return 0 
end
```

## 实现

引入Jedis
```xml
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
    <version>2.9.0</version>
</dependency>
```

```java
@Service
public class RedisTool {

    private static final String LOCK_SUCCESS = "OK";
    private static final String SET_IF_NOT_EXIST = "NX";
    private static final String SET_WITH_EXPIRE_TIME = "PX";
    private static final Long RELEASE_SUCCESS = 1L;

    /**
     * 尝试获取分布式锁
     * @param jedis Redis客户端
     * @param lockKey redis key
     * @param requestId UUID.randomUUID().toString()
     * @param expireTime 过期时间
     * @return 是否获取成功
     */
    public static boolean tryGetDistributedLock(Jedis jedis, String lockKey, String requestId, int expireTime) {
        // 低版本的jedis并不支持多参数的set()方法
        String result = jedis.set(lockKey, requestId, SET_IF_NOT_EXIST, SET_WITH_EXPIRE_TIME, expireTime);
        if (LOCK_SUCCESS.equals(result)) {
            return true;
        }
        return false;
    }

    // 解锁
    public static boolean releaseDistributedLock(Jedis jedis, String lockKey, String requestId) {
        String script = "if redis.call('get', KEYS[1]) == ARGV[1] then return redis.call('del', KEYS[1]) else return 0 end";
        Object result = jedis.eval(script, Collections.singletonList(lockKey), Collections.singletonList(requestId));
        if (RELEASE_SUCCESS.equals(result)) {
            return true;
        }
        return false;
    }
}
```

# 基于redisson实现的分布式锁

```xml
<dependency>
    <groupId>org.redisson</groupId>
    <artifactId>redisson</artifactId>
    <version>3.8.2</version>
</dependency>
```

单机模式
```java
// 构造redisson实现分布式锁必要的Config
Config config = new Config();
config.useSingleServer().setAddress("redis://172.29.1.180:5379").setPassword("a123456").setDatabase(0);
// 构造RedissonClient
RedissonClient redissonClient = Redisson.create(config);
// 设置锁定资源名称
RLock disLock = redissonClient.getLock("DISLOCK");
boolean isLock;
try {
    //尝试获取分布式锁
    isLock = disLock.tryLock(500, 15000, TimeUnit.MILLISECONDS);
    if (isLock) {
        // if get lock success, do something;
        Thread.sleep(15000);
    }
} catch (Exception e) {
} finally {
    // 无论如何, 最后都要解锁
    disLock.unlock();
}
```

哨兵模式
```java
Config config = new Config();
config.useSentinelServers().addSentinelAddress(
        "redis://172.29.3.245:26378","redis://172.29.3.245:26379", "redis://172.29.3.245:26380")
        .setMasterName("mymaster")
        .setPassword("a123456").setDatabase(0);
```

集群模式
```java
Config config = new Config();
config.useClusterServers().addNodeAddress(
        "redis://172.29.3.245:6375","redis://172.29.3.245:6376", "redis://172.29.3.245:6377",
        "redis://172.29.3.245:6378","redis://172.29.3.245:6379", "redis://172.29.3.245:6380")
        .setPassword("a123456").setScanInterval(5000);
```
