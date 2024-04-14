# 内存淘汰策略

Redis 提供了几种内存淘汰策略，当 Redis 的内存使用达到配置的上限时，这些策略决定了哪些 key 应该被移除以释放空间。

以下是 Redis 支持的主要内存淘汰策略：

1. **noeviction**：当内存限制达到后，Redis 不会淘汰任何 key，对于写操作会返回错误, 这是默认的策略
2. **allkeys-lru**：当内存不足时，根据最近最少使用原则，从所有 key 中淘汰最久未被使用的 key
3. **allkeys-random**：从所有 key 中随机选择并淘汰一些 key
4. **volatile-lru**：与 allkeys-lru 类似，但是只会淘汰那些设置了过期时间的 key
5. **volatile-random**：与 allkeys-random 类似，但是只会淘汰那些设置了过期时间的 key
6. **volatile-ttl**：根据 key 的剩余生存时间（TTL）来淘汰，优先淘汰那些剩余生存时间最短的 key
7. **allkeys-lfu**：根据 key 的使用频率来淘汰，优先淘汰那些使用频率最低的 key。这个策略在 Redis 4.0 及以上版本中可用
8. **volatile-lfu**：与 allkeys-lfu 类似，但是只会淘汰那些设置了过期时间的 key。这个策略在 Redis 4.0 及以上版本中可用

LRU（Least Recently Used）: 如果数据项在一段时间内没有被访问，那么在未来被访问的可能性也较低。因此，LRU 算法会选择最长时间未被访问的数据项进行淘汰。

LFU（Least Frequently Used）: LFU 算法则基于数据项的访问频率来决定哪些应该被移除。它保留那些访问频率较高的数据项，并淘汰那些访问频率较低的。LFU 算法认为，经常被访问的数据项在未来也可能被频繁访问。
。
