# 搭建 Redis Cluster

企业级开发中最常用的方法：使用 Docker Compose 配合自定义网络和静态 IP。这样可以彻底解决容器重启后 IP 变化导致的集群崩溃问题。

### 1. docker-compose.yml

新建一个空目录（例如 redis-cluster），在里面创建 docker-compose.yml 文件，填入以下内容：

```yaml
version: "3.8"

# 定义一个自定义网络，并指定子网网段，方便分配静态 IP
networks:
  redis-net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.38.0.0/16

# 使用 YAML 锚点提取公共配置，减少代码冗余
x-redis-common: &redis-common
  image: redis:latest
  restart: always
  # 直接通过启动命令开启集群模式，省去挂载配置文件的麻烦
  command: redis-server --cluster-enabled yes --cluster-config-file nodes.conf --cluster-node-timeout 5000 --appendonly yes
  networks:
    - redis-net

services:
  redis-node-1:
    <<: *redis-common
    container_name: redis-node-1
    ports:
      - "6371:6379" # 客户端连接端口
      - "16371:16379" # 集群节点间通信总线端口 (固定为 6379 + 10000)
    networks:
      redis-net:
        ipv4_address: 172.38.0.11 # 固定 IP

  redis-node-2:
    <<: *redis-common
    container_name: redis-node-2
    ports:
      - "6372:6379"
      - "16372:16379"
    networks:
      redis-net:
        ipv4_address: 172.38.0.12

  redis-node-3:
    <<: *redis-common
    container_name: redis-node-3
    ports:
      - "6373:6379"
      - "16373:16379"
    networks:
      redis-net:
        ipv4_address: 172.38.0.13

  redis-node-4:
    <<: *redis-common
    container_name: redis-node-4
    ports:
      - "6374:6379"
      - "16374:16379"
    networks:
      redis-net:
        ipv4_address: 172.38.0.14

  redis-node-5:
    <<: *redis-common
    container_name: redis-node-5
    ports:
      - "6375:6379"
      - "16375:16379"
    networks:
      redis-net:
        ipv4_address: 172.38.0.15

  redis-node-6:
    <<: *redis-common
    container_name: redis-node-6
    ports:
      - "6376:6379"
      - "16376:16379"
    networks:
      redis-net:
        ipv4_address: 172.38.0.16
```

### 2. 启动所有节点

在 docker-compose.yml 所在的目录下执行：

```sh
docker-compose up -d
```

此时，6 个 Redis 容器已经独立跑起来了，但它们还不是一个集群，只是 6 个互不相干的开启了集群模式的单机。

### 3. 初始化建立集群关系 (核心步骤)

我们需要借助 redis-cli 工具，把这 6 个节点“缝合”在一起。因为我们分配了静态 IP，所以这条命令非常明确。

进入 redis-node-1 容器内部并执行集群创建命令：

```sh
docker exec -it redis-node-1 redis-cli --cluster create \
172.38.0.11:6379 \
172.38.0.12:6379 \
172.38.0.13:6379 \
172.38.0.14:6379 \
172.38.0.15:6379 \
172.38.0.16:6379 \
--cluster-replicas 1
```

参数解析：

- `--cluster create`: 告诉 Redis 开始创建集群。
- `172.38.0.x:6379`: 把这 6 个节点加入集群（注意这里使用的是容器内部默认的 6379 端口，不是宿主机映射端口）。
- `--cluster-replicas 1`: 表示为每个主节点（Master）分配 1 个从节点（Slave）。Redis 会自动计算：6 个节点，每个 Master 带 1 个 Slave，正好分配为 3 主 3 从。

执行后，终端会打印出主从分配计划（Master/Slave 对应关系以及哈希槽的分配），并在最后询问你：

```
Can I set the above configuration? (type 'yes' to accept):
```

输入 yes 并回车。

当看到 `[OK] All 16384 slots covered.` 的提示时，恭喜你，集群搭建成功！

### 4. 验证集群状态与特性

注意，连接集群必须加上 `-c` (cluster) 参数，否则遇到跨节点的数据你将无法操作。

```sh
docker exec -it redis-node-1 redis-cli -c
```

进入命令行后，输入：

```sh
cluster nodes
```

你可以清楚地看到哪 3 个是 master，哪 3 个是 slave，以及它们的槽位（Slots）范围。

#### 测试数据重定向 (Redirect)

试着存入几个不同的 key：

```sh
set name docker
set age 10
set user admin
```

你会发现，随着 key 的不同，Redis 会提示 `Redirected to slot [xxxx] located at 172.38.0.xx:6379`。这说明数据被自动打散并路由到了不同的主节点上，这正是集群的核心魅力所在。
