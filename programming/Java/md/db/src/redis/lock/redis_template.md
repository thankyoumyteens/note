# RedisTemplate 实现

### 1. lua 脚本

```java
private static final String REDIS_LOCK_KEY = "products";
// 获取锁的 Lua 脚本
private static final String LOCK_SCRIPT =
        "if redis.call('setnx', KEYS[1], ARGV[1]) == 1 then " +
                "redis.call('pexpire', KEYS[1], ARGV[2]); " +
                "return true; " +
                "else return false; " +
                "end";

// 释放锁的 Lua 脚本
private static final String UNLOCK_SCRIPT =
        "if redis.call('get', KEYS[1]) == ARGV[1] then " +
                "redis.call('del', KEYS[1]); " +
                "return true; " +
                "else return false; " +
                "end";

// 锁的过期时间
private static final int LOCK_EXPIRE_TIME = 5 * 60 * 1000;
```

### 1. 加锁

```java
/**
 * 加锁, 成功返回true
 */
public static <K, V> boolean lock(RedisTemplate<K, V> rt, String threadId) {
    String[] keys = {REDIS_LOCK_KEY};
    Object[] args = {threadId, LOCK_EXPIRE_TIME};
    RedisScript<Boolean> script = new DefaultRedisScript<>(LOCK_SCRIPT, Boolean.class);
    return rt.execute(script, Arrays.asList(keys), args);
}
```

### 2. 解锁

```java
/**
 * 解锁, 成功返回true
 */
public static boolean unlock(RedisTemplate<K, V> rt, String threadId) {
    String[] keys = {REDIS_LOCK_KEY};
    Object[] args = {threadId};
    RedisScript<Boolean> script = new DefaultRedisScript<>(UNLOCK_SCRIPT, Boolean.class);
    return rt.execute(script, Arrays.asList(keys), args);
}
```
