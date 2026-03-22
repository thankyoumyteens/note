# 开启持久化与设置密码

纯内存运行的 Redis 一旦容器重启，数据就会全部丢失。在实际开发和生产中，我们必须开启数据持久化（AOF/RDB）并设置访问密码。

### 1. 准备目录结构

在宿主机创建用来存放配置和数据的目录（以 ~/tmp/mydata/redis 为例）：

```sh
mkdir -p ~/tmp/mydata/redis/conf
mkdir -p ~/tmp/mydata/redis/data
```

### 2. 准备配置文件 (redis.conf)

Redis 容器默认是不带 redis.conf 文件的。我们需要自己创建一个。

在 ~/tmp/mydata/redis/conf 目录下创建一个名为 redis.conf 的文件：

```sh
touch ~/tmp/mydata/redis/conf/redis.conf
```

然后编辑这个文件（使用 vim 或其他编辑器），写入以下两行最核心的配置：

```sh
# 设置 Redis 连接密码 (把 yourpassword 换成你想要的密码)
requirepass yourpassword

# 开启 AOF 持久化，确保数据不会因为重启而丢失
appendonly yes
```

### 3. 带着配置和挂载目录启动容器

如果你之前跑了阶段一的容器，记得先 `docker rm -f my-redis` 删掉它，避免名字和端口冲突

```sh
docker run -p 6379:6379 \
  --name my-redis \
  -v ~/tmp/mydata/redis/conf/redis.conf:/etc/redis/redis.conf \
  -v ~/tmp/mydata/redis/data:/data \
  --restart always \
  -d redis redis-server /etc/redis/redis.conf
```

关键参数解释：

- `-v .../data:/data`: 将容器内默认产生数据的 `/data` 目录挂载到宿主机。
- `redis-server /etc/redis/redis.conf`: 这是告诉 Redis 容器，启动时请使用我们挂载进去的这个配置文件。
