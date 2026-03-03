# Redis Cluster

### 1. 下载解压源码

Redis 源码中自带了一个用于测试的脚本，可以一键启动 6 个节点（3 主 3 从）

```sh
wget https://mirrors.huaweicloud.com/redis/redis-7.2.4.tar.gz
tar -zxvf redis-7.2.4.tar.gz
```

### 2. 编译

```sh
cd ./redis-7.2.4
make
```

编译完成后，src 目录下就会出现 redis-server 进程文件

### 3. 启动并创建集群

```sh
cd ./redis-7.2.4/utils/create-cluster

# 启动 6 个 Redis 实例
./create-cluster start

# 将实例组建成集群 (输入 'yes' 确认分配)
./create-cluster create
```

## 手动创建集群

```sh
# 开启 6 个终端窗口，或者后台运行：
redis-server --port 30001 --cluster-enabled yes --cluster-config-file nodes-30001.conf --daemonize yes
redis-server --port 30002 --cluster-enabled yes --cluster-config-file nodes-30002.conf --daemonize yes
redis-server --port 30003 --cluster-enabled yes --cluster-config-file nodes-30003.conf --daemonize yes
redis-server --port 30004 --cluster-enabled yes --cluster-config-file nodes-30004.conf --daemonize yes
redis-server --port 30005 --cluster-enabled yes --cluster-config-file nodes-30005.conf --daemonize yes
redis-server --port 30006 --cluster-enabled yes --cluster-config-file nodes-30006.conf --daemonize yes

# 然后执行集群创建
redis-cli --cluster create 127.0.0.1:30001 127.0.0.1:30002 127.0.0.1:30003 127.0.0.1:30004 127.0.0.1:30005 127.0.0.1:30006 --cluster-replicas 1
```
