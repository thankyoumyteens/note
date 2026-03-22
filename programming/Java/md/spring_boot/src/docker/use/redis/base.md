# 最基础的 Redis 运行

### 1. 拉取 Redis 镜像

```sh
docker pull redis:latest
```

### 2. 启动 Redis 容器

```sh
docker run --name my-redis -p 6379:6379 -d redis
```

参数解释：

- `-p 6379:6379`: 将宿主机的 6379 端口映射到容器内的 6379 端口（Redis 默认端口）。

### 3. 测试是否运行成功

你可以直接进入容器内部使用自带的命令行工具（redis-cli）测试：

```sh
docker exec -it my-redis redis-cli
```

进入后输入 `ping`，如果返回 PONG，说明 Redis 已经正常工作了！输入 exit 可以退出。
