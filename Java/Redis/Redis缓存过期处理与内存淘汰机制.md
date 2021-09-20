# key过期处理

设置了expire的key缓存过期了，但是服务器的内存还是会被占用，这是因为redis所基于的两种删除策略

## （主动）定时删除

定时随机的检查过期的key，如果过期则清理删除。

redis.conf
```conf
# 每秒钟检测10次
hz 10
```

## （被动）惰性删除

当客户端请求一个已经过期的key的时候，那么redis会检查这个key是否过期，如果过期了，则删除，然后返回一个nil。这种策略
友好，不会有太多的损耗，但是内存占用会比较高。

# 缓存淘汰机制

所以，当内存占用满了以后，redis提供了一套缓存淘汰机制

redis.conf
```conf
maxmemory noeviction
```

maxmemory: 当内存已使用率到达，则开始清理缓存, 可用的清理算法如下:

* noeviction: 旧缓存永不过期，新缓存设置不了，返回错误
* allkeys-lru: 清除最少用的旧缓存，然后保存新的缓存（推荐使用）
* allkeys-random: 在所有的缓存中随机删除（不推荐）
* volatile-lru: 在那些设置了expire过期时间的缓存中，清除最少用的旧缓存，然后保存新的缓存
* volatile-random: 在那些设置了expire过期时间的缓存中，随机删除缓存
* volatile-ttl: 在那些设置了expire过期时间的缓存中，删除即将过期的
