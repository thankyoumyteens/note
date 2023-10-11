# 安装依赖包

```sh
sudo apt install -y build-essential tcl
```

# 下载Redis源代码

```sh
cd ~/src_pack
curl -O http://download.redis.io/redis-stable.tar.gz
tar -xzvf redis-stable.tar.gz
```

# 编译安装

```sh
cd redis-stable
sudo make
sudo make test
sudo make install
```

# 直接启动

```sh
# 加上‘&’号使redis以后台程序方式运行
/usr/local/bin/redis-server &
```

# 通过指定配置文件启动

```sh
/usr/local/bin/redis-server /etc/redis/6379.conf
```

如果更改了端口, 使用`redis-cli`客户端连接时, 也需要指定端口, 例如：

```sh
redis-cli -p 6380
```
