# 使用Lua的好处

- Lua脚本在Redis中是原子执行的, 执行过程中间不会插入其他命令
- Lua脚本可以帮助开发和运维人员创造出自己定制的命令, 并可以将这些命令常驻在Redis内存中, 实现复用的效果
- Lua脚本可以将多条命令一次性打包, 有效地减少网络开销

# 在Redis执行Lua脚本

## eval

语法
```
eval 脚本内容 key个数 key列表 参数列表
```

参数说明: 
- 脚本内容: 参数是一段 Lua 5.1 脚本程序。脚本不必(也不应该)定义为一个 Lua 函数。
- key个数: 用于指定键名参数的个数。当脚本不需要任何参数时, 也不能省略这个参数(设为0)
- key列表: 表示在脚本中所用到的那些 Redis 键(key), 这些键名参数可以在 Lua 中通过全局变量 KEYS 数组, 用 1 为基址的形式访问(`KEYS[1]`,  `KEYS[2]`, 以此类推)
- 参数列表: 附加参数, 在 Lua 中通过全局变量 ARGV 数组访问, 访问的形式和 KEYS 变量类似(`ARGV[1]`, `ARGV[2]`, 诸如此类)。

例子
```bash
127.0.0.1:6379> eval 'return "hello " ..KEYS[1]..ARGV[1]' 1 redis world
"hello redisworld"
```

## redis-cli --eval

如果Lua脚本较长, 还可以使用redis-cli–eval直接执行文件

编写lua脚本
```
/tmp/test.lua
```
执行脚本
```
redis-cli --eval /tmp/test.lua , 10
```

`--eval`参数是告诉redis-cli读取并运行后面的Lua脚本, `/tmp/test.lua`是脚本的位置, 后面跟着是传给Lua脚本的参数。

其中`,`前的是要操作的键, 可以再脚本中用`KEYS[index]`获取, `,`后面的`10`是参数, 在脚本中能够使用`ARGV[index]`获得。注: `,`两边的空格不能省略, 否则会出错

## evalsha

首先用script load命令将Lua脚本加载到Redis服务端, 得到该脚本的SHA1校验和, evalsha命令使用SHA1作为参数可以直接执行对应Lua脚本, 避免每次发送Lua脚本的开销。这样客户端就不需要每次执行脚本内容, 而脚本也会常驻在服务端, 脚本功能得到了复用

语法
```
evalsha 脚本的SHA1值 key个数 key列表 参数列表
```

新建脚本文件
```bash
vim lua_test.lua
```
输入脚本内容, 保存
```lua
return "hello" ..KEYS[1]..ARGV[1]
```
加载脚本
```bash
redis-cli script load "$(cat lua_test.lua)"
# 输出: "af54f206bd1c4e5de6b4a1edefa9b22622ea0805"
```
执行脚本
```bash
redis-cli
127.0.0.1:6379> evalsha af54f206bd1c4e5de6b4a1edefa9b22622ea0805 1 redis world
"helloredisworld"
```

## 其他命令

### script exists

根据脚本的校验码, 校验指定的脚本是否已经被保存在缓存当中

语法
```
127.0.0.1:6379> script exists script [script ...]
```

返回值

一个列表, 包含 0 和 1 , 前者表示脚本不存在于缓存, 后者表示脚本已经在缓存里面了。

### script flush

用于清除所有 Lua 脚本缓存

语法
```
127.0.0.1:6379> script flush
```

### script kill

用于杀死当前正在运行的 Lua 脚本, 当且仅当这个脚本没有执行过任何写操作时, 这个命令才生效。这个命令主要用于终止运行时间过长的脚本, 比如一个因为 BUG 而发生无限循环的脚本。

语法
```
redis 127.0.0.1:6379> script kill
```

# 在Lua中执行Redis命令

Lua可以使用redis.call函数实现对Redis的访问, 例如下面代码是Lua使用redis.call调用了Redis的set和get操作
```lua
redis.call("set", "hello", "world")
redis.call("get", "hello")
```
放在Redis的执行效果如下
```bash
127.0.0.1:6379> eval 'return redis.call("get", KEYS[1])' 1 hello
"world"
```

除此之外Lua还可以使用redis.pcall函数实现对Redis的调用, 

redis.call和redis.pcall的不同在于, 如果redis.call执行失败, 那么脚本执行结束会直接返回错误, 

而redis.pcall会忽略错误继续执行脚本

在 Lua 脚本中, 可以通过调用 redis.log 函数来写 Redis 日志(log)
```
redis.log(loglevel, message)
```
其中,  message 参数是一个字符串, 而 loglevel 参数可以是以下任意一个值
- redis.LOG_DEBUG
- redis.LOG_VERBOSE
- redis.LOG_NOTICE

上面的这些等级(level)和标准 Redis 日志的等级相对应
