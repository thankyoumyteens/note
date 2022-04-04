# ubuntu 源码安装redis

安装基本的编译工具
```
sudo apt install build-essential tcl
```

下载Redis源代码
```
curl -O http://download.redis.io/redis-stable.tar.gz
```

解压tar包
```
tar xzvf redis-stable.tar.gz
```

编译安装
```
cd redis-stable
make
make test
sudo make install
```

# 直接启动

进入redis根目录, 执行命令:
```
# 加上‘&’号使redis以后台程序方式运行
./redis-server &
```

# 通过指定配置文件启动

进入redis根目录, 输入命令：
```
./redis-server /etc/redis/6379.conf
```

如果更改了端口, 使用`redis-cli`客户端连接时, 也需要指定端口, 例如：
```
redis-cli -p 6380
```

# 使用redis启动脚本设置开机自启动

启动脚本 redis_init_script 位于位于Redis的 /utils/ 目录下，redis_init_script脚本代码如下

```sh
#!/bin/sh
#
# Simple Redis init.d script conceived to work on Linux systems
# as it does use of the /proc filesystem.
 
#redis服务器监听的端口
REDISPORT=6379
#服务端所处位置
EXEC=/usr/local/bin/redis-server
#客户端位置
CLIEXEC=/usr/local/bin/redis-cli
#redis的PID文件位置，需要修改
PIDFILE=/var/run/redis_${REDISPORT}.pid
#redis的配置文件位置，需将${REDISPORT}修改为文件名
CONF="/etc/redis/${REDISPORT}.conf"
case "$1" in
    start)
        if [ -f $PIDFILE ]
        then
                echo "$PIDFILE exists, process is already running or crashed"
        else
                echo "Starting Redis server..."
                $EXEC $CONF
        fi
        ;;
    stop)
        if [ ! -f $PIDFILE ]
        then
                echo "$PIDFILE does not exist, process is not running"
        else
                PID=$(cat $PIDFILE)
                echo "Stopping ..."
                $CLIEXEC -p $REDISPORT shutdown
                while [ -x /proc/${PID} ]
                do
                    echo "Waiting for Redis to shutdown ..."
                    sleep 1
                done
                echo "Redis stopped"
        fi
        ;;
    *)
        echo "Please use start or stop as first argument"
        ;;
esac
```

将修改好的配置文件复制到指定目录下

```
cp redis.conf /etc/redis/6379.conf
```

将启动脚本复制到/etc/init.d目录下

```
cp redis_init_script /etc/init.d/redisd
```

在启动脚本开头添加如下注释来修改运行级别

```sh
#!/bin/sh
# chkconfig:   2345 90 10
```

设置为开机自启动

```
chkconfig redisd on
```
