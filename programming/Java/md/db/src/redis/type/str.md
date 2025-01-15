# 字符串

redis 的字符串类型不仅可以存字符串, 还可以存储数字类型。

字符串 value 最大不能超过 512MB。

常用场景:

- 缓存
- 计数器
- 分布式锁

## 字符串操作

```sh
# 存储一条key为name, value为zhangsan的数据
# 无论key是否存在, 都会设置
set name "zhangsan"

# 只有key不存在时, 才设置
setnx name "zhangsan"

# 只有key存在时, 才设置
set name "zhangsan" xx

# 设置新值为zhangsan, 并返回旧值
getset name "zhangsan"

# 把!!!追加到name的旧值上
append name "!!!"

# 获取key为name的值的长度
strlen name

# 获取key为name的value
get key

# 删除key为name的数据
del name
```

## 数字类型操作

因为 redis 是单线程的, 所以用来做计数器不用考虑线程安全问题。

```sh
# 把key为global_counter的value自增1
# 如果key不存在, 则创建, 并从0开始自增
incr global_counter

# 把key为global_counter的value自减1
# 如果key不存在, 则创建, 并从0开始自减
decr global_counter

# 把key为global_counter的value自增233
# 如果key不存在, 则创建, 并从0开始自增
incrby global_counter 233

# 把key为global_counter的value自减333
# 如果key不存在, 则创建, 并从0开始自减
decrby global_counter 333
```

## 批量操作

减少和 redis 服务器的交互次数。

```sh
# 批量设置
mset key1 value1 key2 value2 key3 value3 ...

# 批量获取
mget key1 key2 key3 ...
```
