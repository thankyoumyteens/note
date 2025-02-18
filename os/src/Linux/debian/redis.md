# 安装 redis

### 1. 下载解压源码:

```sh
wget https://mirrors.huaweicloud.com/redis/redis-6.0.9.tar.gz
tar -zxvf redis-6.0.9.tar.gz
cd redis-6.0.9
```

### 2. 修改 `src/Makefile` 文件:

```sh
# 修改安装路径 默认/usr/local
PREFIX?=/software/redis-6.0.9
INSTALL_BIN=$(PREFIX)
```

### 3. 安装:

```sh
make
make install
```

### 4. 配置环境变量

```sh
# 打开配置文件
sudo vim /etc/profile

# 在最后一行添加
export PATH=/software/redis-6.0.9/bin:$PATH

# 使环境变量生效
source /etc/profile
```

### 5. 允许远程连接

```sh
# 配置文件在源码根目录
cp redis.conf /software/redis.conf
vim /software/redis.conf
# 把 bind 127.0.0.1 改成 bind 0.0.0.0
# 把 protected-mode yes 改成 protected-mode no
# 把 daemonize no 改成 daemonize yes

# 启动
nohup redis-server /software/redis.conf &
```
