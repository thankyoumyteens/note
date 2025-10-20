# 通用操作

```py
# 设置键值（默认永不过期）
connection.set('name', 'Alice')

# 设置键值并指定过期时间
connection.setex('age', 30, 25)  # 方式1
connection.set('city', 'Beijing', ex=60)  # 方式2（ex=秒，px=毫秒）

# 判断键是否存在
print(connection.exists('name'))  # 存在返回1，否则0

# 获取键的过期时间（-1：永不过期，-2：键不存在）
print(connection.ttl('age'))  # 剩余过期时间（秒）

# 删除键
connection.delete('city')

# 查看所有键（谨慎使用，生产环境可能数据量大）
print(connection.keys('*'))  # 返回所有键的列表

# 获取键的类型
print(connection.type('name'))  # 输出：string

# 重命名键
connection.rename('old_key', 'new_key')

# 移动键到其他数据库
connection.move('name', 1)  # 将name键从当前库移动到数据库1

# 清空当前数据库
connection.flushdb()

# 清空所有数据库
connection.flushall()
```
