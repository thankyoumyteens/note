# 字符串类型 string
- 存储： `set key value`
```
127.0.0.1:6379> set username zhangsan
OK
```
- 获取： `get key`
```
127.0.0.1:6379> get username
"zhangsan"
```
- 删除： `del key`
```
127.0.0.1:6379> del age
(integer) 1
```

# 哈希类型 hash
- 存储： `hset key field value`
```
127.0.0.1:6379> hset myhash username lisi
(integer) 1
127.0.0.1:6379> hset myhash password 123
(integer) 1
```
- 获取指定的field对应的值： `hget key field`
```
127.0.0.1:6379> hget myhash username
"lisi"
```
- 获取所有的field和value： `hgetall key`
```
127.0.0.1:6379> hgetall myhash
1) "username"
2) "lisi"
3) "password"
4) "123"
```
- 删除： `hdel key field`
```
127.0.0.1:6379> hdel myhash username
(integer) 1
```

# 列表类型 list
可以添加一个元素到列表的头部（左边）或者尾部（右边）

- 将元素加入列表左表: `lpush key value`
- 将元素加入列表右边: `rpush key value`
```
127.0.0.1:6379> lpush myList a
(integer) 1
127.0.0.1:6379> lpush myList b
(integer) 2
127.0.0.1:6379> rpush myList c
(integer) 3
```
- 范围获取： `lrange key start end`
```
127.0.0.1:6379> lrange myList 0 -1
1) "b"
2) "a"
3) "c"
```
- 删除列表最左边的元素, 并将元素返回: `lpop key` 
- 删除列表最右边的元素, 并将元素返回: `rpop key`

# 集合类型 set
- 存储：`sadd key value`
```
127.0.0.1:6379> sadd myset a
(integer) 1
127.0.0.1:6379> sadd myset a
(integer) 0
```
- 获取set集合中所有元素：`smembers key`
```
127.0.0.1:6379> smembers myset
1) "a"
```
- 删除：`srem key value`
```	
127.0.0.1:6379> srem myset a
(integer) 1
```

# 有序集合类型 sortedset
不允许重复元素, 且元素有顺序.每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。

- 存储：`zadd key score value`
```
127.0.0.1:6379> zadd mysort 60 zhangsan
(integer) 1
127.0.0.1:6379> zadd mysort 50 lisi
(integer) 1
127.0.0.1:6379> zadd mysort 80 wangwu
(integer) 1
```
- 获取：`zrange key start end [withscores]`
```
127.0.0.1:6379> zrange mysort 0 -1
1) "lisi"
2) "zhangsan"
3) "wangwu"

127.0.0.1:6379> zrange mysort 0 -1 withscores
1) "zhangsan"
2) "60"
3) "wangwu"
4) "80"
5) "lisi"
6) "500"
```
- 删除：`zrem key value`
```
127.0.0.1:6379> zrem mysort lisi
(integer) 1
```
