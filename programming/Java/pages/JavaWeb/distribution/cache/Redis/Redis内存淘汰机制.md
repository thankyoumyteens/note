# 缓存淘汰机制

当内存占用满了以后, redis提供了一套缓存淘汰机制

redis.conf
```conf
maxmemory noeviction
```

maxmemory: 当内存已使用率到达, 则开始清理缓存

可用的清理算法如下:

- no-eviction: 当内存不足以容纳新写入数据时, 新的写入操作会报错
- allkeys-lru: 当内存不足以容纳新写入数据时, 移除最近最少使用的key(这个是最常用的)
- allkeys-random: 当内存不足以容纳新写入数据时, 随机移除某个key
- volatile-lru: 当内存不足以容纳新写入数据时, 在设置了过期时间的key中, 移除最近最少使用的key
- volatile-random: 当内存不足以容纳新写入数据时, 在设置了过期时间的key中, 随机移除某个key
- volatile-ttl: 当内存不足以容纳新写入数据时, 在设置了过期时间的key中, 有更早过期时间的key优先移除
