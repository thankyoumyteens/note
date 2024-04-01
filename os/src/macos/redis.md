# 安装 redis

下载解压源码:

```sh
wget https://mirrors.huaweicloud.com/redis/redis-7.2.4.tar.gz
tar -zxvf redis-7.2.4.tar.gz
```

修改 src/Makefile 文件:

```sh
# 改成安装路径
PREFIX?=/Users/walter/walter/software/redis
INSTALL_BIN=$(PREFIX)
```

安装:

```sh
make
make install
```

## 配置环境变量

1. 打开配置文件

```sh
vim ~/.zshrc
```

2. 在最后一行添加:

```conf
export PATH=/Users/walter/walter/software/redis:$PATH
```

3. 使环境变量生效

```sh
source ~/.zshrc
```
