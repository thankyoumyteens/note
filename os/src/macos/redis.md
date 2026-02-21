# Redis

### 1. 下载解压源码

```sh
wget https://mirrors.huaweicloud.com/redis/redis-7.2.4.tar.gz
tar -zxvf redis-7.2.4.tar.gz
cd redis-7.2.4
```

### 2. 修改 `src/Makefile` 文件

```sh
# 修改安装路径
PREFIX?=/Users/walter/walter/software/redis
INSTALL_BIN=$(PREFIX)
```

### 3. 安装

```sh
make
make install
```

### 4. 配置环境变量

```sh
# 打开配置文件
vim ~/.zshrc

# 在最后一行添加
export PATH=/Users/walter/walter/software/redis:$PATH

# 使环境变量生效
source ~/.zshrc
```

## 报错: call to undeclared function 'fstat64';

修改 src/config.h 文件

```c
#ifdef __APPLE__
// 新增
#define _DARWIN_C_SOURCE
```
