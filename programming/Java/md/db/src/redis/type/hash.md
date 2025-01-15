# hash

redis 的 hash 相当于 `Map<String, Map<String, Object>>` 类型。

```sh
# 设置
hset student name "zhangsan"
hset student age 18

# 获取某个属性(field)
hget student name

# 列出所有属性
hgetall student

# 删除某个属性
hdel student name

# 判断某个属性是否存在
hexists student name

# 获取有多少个属性
hlen student
```

## 批量操作

```sh
# 批量设置
hmset key field1 value1 field2 value2 field3 value3 ...

# 批量获取
hmget key field1 field2 field3 ...
```
