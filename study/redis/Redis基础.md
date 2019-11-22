# redis的启动方式

1. 直接启动: 进入redis根目录，执行命令:
    ```
    # 加上‘&’号使redis以后台程序方式运行
    ./redis-server &
    ```
2. 通过指定配置文件启动: 进入redis根目录，输入命令：
    ```
    ./redis-server /etc/redis/6379.conf
    ```
3. 如果更改了端口，使用`redis-cli`客户端连接时，也需要指定端口，例如：
    ```
    redis-cli -p 6380
    ```

# 设置redis访问（AUTH）密码

需要永久配置密码的话就去redis.conf的配置文件中找到`requirepass`这个参数，如下配置：

修改redis.conf配置文件　　
```
# requirepass foobared
requirepass 123
```
保存后重启redis就可以了

# Redis数据类型

1. 字符串类型 string
2. 哈希类型 hash
3. 列表类型 list
4. 集合类型 set
5. 有序集合类型 sortedset

# redis的应用场景

* 缓存（数据查询、短连接、新闻内容、商品内容等等）
* 聊天室的在线好友列表
* 任务队列。（秒杀、抢购、12306等等）
* 应用排行榜
* 网站访问统计
* 数据过期处理（可以精确到毫秒
* 分布式集群架构中的session分离

# 字符串类型 string
1. 存储： `set key value`
    ```
    127.0.0.1:6379> set username zhangsan
    OK
    ```
2. 获取： `get key`
    ```
    127.0.0.1:6379> get username
    "zhangsan"
    ```
3. 删除： `del key`
    ```
    127.0.0.1:6379> del age
    (integer) 1
    ```

# 哈希类型 hash
1. 存储： `hset key field value`
    ```
    127.0.0.1:6379> hset myhash username lisi
    (integer) 1
    127.0.0.1:6379> hset myhash password 123
    (integer) 1
    ```
2. 获取指定的field对应的值： `hget key field`
    ```
    127.0.0.1:6379> hget myhash username
    "lisi"
    ```
3. 获取所有的field和value： `hgetall key`
    ```
    127.0.0.1:6379> hgetall myhash
    1) "username"
    2) "lisi"
    3) "password"
    4) "123"
    ```
4. 删除： `hdel key field`
    ```
    127.0.0.1:6379> hdel myhash username
    (integer) 1
    ```

# 列表类型 list
可以添加一个元素到列表的头部（左边）或者尾部（右边）

1. 将元素加入列表左表: `lpush key value`
2. 将元素加入列表右边: `rpush key value`
    ```
    127.0.0.1:6379> lpush myList a
    (integer) 1
    127.0.0.1:6379> lpush myList b
    (integer) 2
    127.0.0.1:6379> rpush myList c
    (integer) 3
    ```
3. 范围获取： `lrange key start end`
    ```
    127.0.0.1:6379> lrange myList 0 -1
    1) "b"
    2) "a"
    3) "c"
    ```
4. 删除列表最左边的元素，并将元素返回: `lpop key` 
5. 删除列表最右边的元素，并将元素返回: `rpop key`

# 集合类型 set
1. 存储：`sadd key value`
    ```
    127.0.0.1:6379> sadd myset a
    (integer) 1
    127.0.0.1:6379> sadd myset a
    (integer) 0
    ```
2. 获取set集合中所有元素：`smembers key`
    ```
    127.0.0.1:6379> smembers myset
    1) "a"
    ```
3. 删除：`srem key value`
    ```	
    127.0.0.1:6379> srem myset a
    (integer) 1
    ```

# 有序集合类型 sortedset
不允许重复元素，且元素有顺序.每个元素都会关联一个double类型的分数。redis正是通过分数来为集合中的成员进行从小到大的排序。

1. 存储：`zadd key score value`
    ```
    127.0.0.1:6379> zadd mysort 60 zhangsan
    (integer) 1
    127.0.0.1:6379> zadd mysort 50 lisi
    (integer) 1
    127.0.0.1:6379> zadd mysort 80 wangwu
    (integer) 1
    ```
2. 获取：`zrange key start end [withscores]`
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
3. 删除：`zrem key value`
    ```
    127.0.0.1:6379> zrem mysort lisi
    (integer) 1
    ```

# 通用命令
1. 查询所有的键: `keys *`
2. 获取键对应的value的类型: `type key` 
3. 删除指定的key value: `del key`
