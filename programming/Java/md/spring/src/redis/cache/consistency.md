# 双写一致性

双写一致性: 更新/删除接口修改数据库的数据时, 缓存中的数据也要和数据库保持一致。

先删除缓存, 再修改数据库的问题:

1. 缓存中的数据: {key: 'num', value: 100}
2. 线程 1 删除缓存, 此时线程切换
3. 线程 2 读取数据: {key: 'num', value: 100}
4. 线程 2 写入缓存: {key: 'num', value: 100}
5. 切换回线程 1 , 线程 1 更新数据库: {key: 'num', value: 200}
6. 此时缓存和数据库中的数据不一致

先修改数据库, 再删除缓存的问题:

1. 缓存中的数据: 空
2. 线程 1 读取数据: {key: 'num', value: 100}, 此时线程切换
3. 线程 2 更新数据库: {key: 'num', value: 200}
4. 线程 2 删除缓存
5. 切换回线程 1 , 线程 1 写入缓存: {key: 'num', value: 100}
6. 此时缓存和数据库中的数据不一致

延时双删:

1. 删除缓存
2. 更新数据库
3. 当前线程休眠一段时间, 确保数据已经持久化到数据库中(比如主从结构, 等待主节点同步数据到从节点)
4. 再次删除缓存, 防止在休眠期间有其他线程重新缓存了旧的数据

延迟双删策略的延时时间不好控制, 如果设置不好, 数据库没有同步完成, 依然会有数据不一致的问题。

## 保证强一致性

### 使用分布式锁(性能差)

| 线程 1   | 线程 2 |
| -------- | ------ |
| 加锁     | -      |
| 写数据库 | 等待锁 |
| 删缓存   | -      |
| 解锁     | -      |
| -        | 加锁   |
| -        | 读缓存 |
| -        | 解锁   |

### 使用读写锁优化(性能强一点)

读写锁会保证一定能读到最新数据。写锁是一个排他锁, 读锁是一个共享锁。加写锁前, 需要等待所有读锁释放。加读锁前, 需要等待写锁释放。

| 线程 1 | 线程 2 | 线程 3   | 线程 4   |
| ------ | ------ | -------- | -------- |
| 加读锁 | -      | -        | -        |
| 读缓存 | 加读锁 | -        | -        |
| 解读锁 | 读缓存 | 等待读锁 | -        |
| -      | 解读锁 | -        | -        |
| -      | -      | 加写锁   |          |
| -      | -      | 写数据库 | -        |
| -      | -      | 删缓存   | 等待写锁 |
| -      | -      | 解写锁   | -        |
| -      | -      | -        | 加读锁   |
| -      | -      | -        | 读缓存   |
| -      | -      | -        | 解读锁   |

### redisson 的读写锁用法

```java
public void writeValue(String key, String value) {
    RReadwriteLock lock = redisson.getReadwriteLock("rw-lock");
    RLock wLock = lock.writeLock();
    try {
        wLock.lock();
        redisTemplate.opsForValue().set(key, value);
    } catch (Exception e) {
        e.printstackTrace();
    } finally {
        wLock.unlock();
    }
}

public String readValue(String key) {
    RReadwriteLock lock = redisson.getReadwriteLock("rw-lock");
    RLock rLock = lock.readLock();
    try {
        rLock.lock();
        return redisTemplate.opsForValue().get(key);
    } catch (Exception e) {
        e.printstackTrace();
        return null;
    } finally {
        rLock.unlock();
    }
}
```

## 保证最终一致性

异步通知: 修改数据库后发送消息到 MQ, 缓存服务监听 MQ 消息来更新缓存。
