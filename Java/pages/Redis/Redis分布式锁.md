# SETNX + EXPIRE

SETNX 是SET IF NOT EXISTS的简写，只在key不存在的情况下，才将键key的值设置为value。如果 key不存在，则SETNX成功返回1，如果这个key已经存在了，则返回0。

lock_value是uuid，释放锁时要判断lock_value是否为当前线程设置的uuid值，避免锁过期释放了，业务还没执行完，删了别的线程的锁

```java
// 加锁，lock_value是uuid
if（jedis.setnx(key_resource_id, lock_value) == 1) {
   // 设置过期时间
   expire(key_resource_id，100);
   try {
      // do something
   } catch() {
   } finally {
      // 释放锁
      // 避免锁过期释放了，业务还没执行完，删了别的线程的锁
      if (lock_value.equals(jedis.get(key_resource_id))) {
         jedis.del(key_resource_id);
      }
   }
}
```
问题：如果执行完setnx加锁，还没执行expire设置过期时间时，进程终止了，那么这个锁就不会被释放了

# Lua脚本 + SETNX + EXPIRE

Redis采用同一个Lua解释器去运行所有命令，所以Lua脚本的执行是原子性的。

```java
String lua_scripts = "if redis.call('setnx',KEYS[1],ARGV[1]) == 1 then" +
            " redis.call('expire',KEYS[1],ARGV[2]) return 1 else return 0 end";   
Object result = jedis.eval(lua_scripts, Collections.singletonList(key_resource_id), Collections.singletonList(values));
//判断是否成功
return result.equals(1L);
```

# SET指令扩展参数

用一条SET代替SETNX + EXPIRE两条命令
```
SET key value[EX seconds][PX milliseconds][NX|XX]
```

- NX：key不存在的时候，才能set成功
- XX：key存在的时候，才能set成功
- EX seconds：设定key的过期时间，时间单位是秒。
- PX milliseconds：设定key的过期时间，单位为毫秒

```java
// 加锁，lock_value是uuid
if（jedis.set(key_resource_id, lock_value, "NX", "EX", 100) == 1) {
   try {
      // do something
   }catch() {
   }
   finally {
      // 避免锁过期释放了，业务还没执行完，删了别的线程的锁
      if (lock_value.equals(jedis.get(key_resource_id))) {
         jedis.del(key_resource_id);
      }
   }
}
```

为了更严谨，释放锁也是用lua脚本代替
```java
String lua_scripts = "if redis.call('get',KEYS[1]) == ARGV[1] then" +
         " redis.call('del',KEYS[1]) return 1 else return 0 end";
Object result = jedis.eval(lua_scripts, 
         Collections.singletonList(key_resource_id), 
         Arrays.asList(lock_value, end_time));
//判断是否成功
return result.equals(1L);
```

# Redisson分布式锁

上面集中方案都有锁过期释放，业务没执行完的问题。

解决方法：给获得锁的线程，开启一个定时守护线程，每隔一段时间检查锁是否还存在，存在则对锁的过期时间延长，防止锁过期提前释放。

只要线程一加锁成功，Redisson就会启动一个watch dog，它是一个后台线程，会每隔10秒检查一下，如果线程1还持有锁，那么就会不断的延长锁key的生存时间。

## 单机模式

```java
// 构造redisson实现分布式锁必要的Config
Config config = new Config();
config.useSingleServer()
    .setAddress("redis://172.29.1.180:5379")
    .setPassword("a123456")
    .setDatabase(0);
// 构造RedissonClient
RedissonClient redissonClient = Redisson.create(config);
// 设置锁定资源名称
RLock disLock = redissonClient.getLock("DISLOCK");
boolean isLock;
try {
    //尝试获取分布式锁
    isLock = disLock.tryLock(500, 15000, TimeUnit.MILLISECONDS);
    if (isLock) {
        //if get lock success, do something;
    }
} catch (Exception e) {
} finally {
    // 解锁
    disLock.unlock();
}
```

## 哨兵模式

```java
Config config = new Config();
config.useSentinelServers().addSentinelAddress(
        "redis://172.29.3.245:26378","redis://172.29.3.245:26379", "redis://172.29.3.245:26380")
        .setMasterName("mymaster")
        .setPassword("a123456").setDatabase(0);
```

## 集群模式

```java
Config config = new Config();
config.useClusterServers().addNodeAddress(
        "redis://172.29.3.245:6375","redis://172.29.3.245:6376", "redis://172.29.3.245:6377",
        "redis://172.29.3.245:6378","redis://172.29.3.245:6379", "redis://172.29.3.245:6380")
        .setPassword("a123456").setScanInterval(5000);
```
