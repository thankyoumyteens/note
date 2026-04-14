# 使用 Docker Compose

同样地，为了方便日后管理和一键部署，我们将上述复杂的命令转化为 docker-compose.yml 文件。

### 1. 创建 docker-compose.yml 文件

在你喜欢的目录下创建该文件，并确保同级目录下有 conf/redis.conf 和 data 文件夹。

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

### 2. 一键启动

在这个文件所在的目录下，运行：

```sh
docker-compose up -d
```

### 3. 验证持久化和密码是否生效

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

### 4. 停止并删除容器

想要停止并删除容器，只需运行：

```sh
docker-compose down
```
