# 使用 Docker Compose

同样地，为了方便日后管理和一键部署，我们将上述复杂的命令转化为 docker-compose.yml 文件。

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

### 3. 创建 docker-compose.yml 文件

在 conf 和 data 文件夹的同级目录下创建该文件。

```sh
version: '3.8'

services:
  redis:
    image: redis:latest
    container_name: my-redis
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - ./conf/redis.conf:/etc/redis/redis.conf
      - ./data:/data
    # 覆盖容器启动时的默认命令，指定配置文件启动
    command: redis-server /etc/redis/redis.conf
    environment:
      - TZ=Asia/Shanghai
```

### 4. 一键启动

在这个文件所在的目录下，运行：

```sh
docker-compose up -d
```

### 5. 验证持久化和密码是否生效

```sh
# 进入容器并连接 redis-cli
docker exec -it my-redis redis-cli

# 尝试输入 ping，会报错 (NOAUTH Authentication required)
ping

# 输入密码进行认证 (假设你的密码是 yourpassword)
auth yourpassword

# 再次 ping，就会返回 PONG
ping
```

### 6. 停止并删除容器

想要停止并删除容器，只需运行：

```sh
docker-compose down
```
