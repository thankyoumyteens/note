# 安装 Erlang

将安装包下载到 /home/erlang 目录下。
```
wget http://www.erlang.org/download/otp_src_R16B02.tar.gz
```
解压
```
tar -zxvf otp_src_R16B02.tar.gz
```
编译安装
```
cd otp_src_R16B02
yum -y install make gcc gcc-c++ kernel-devel m4 ncurses-devel openssl-devel
./configure --prefix=/usr/local/erlang --enable-hipe --enable-threads --enable-smp-support --enable-kernel-poll
make
make install
```
配置环境变量
```
vim /etc/profile
```
```
ERL_HOME=/usr/local/erlang
PATH=$ERL_HOME/bin:$PATH
```
使环境变量生效: 
```
source /etc/profile
```
验证
```
erl
```

# 安装 RabbitMQ

下载安装包
```
wget http://www.rabbitmq.com/releases/rabbitmq-server/v3.1.5/rabbitmq-server-3.1.5.tar.gz 
```
解压
```
tar -zxvf rabbitmq-server-3.1.5.tar.gz
```
编译安装
```
cd rabbitmq-server-3.1.5 
yum -y install xmlto 
make
make install TARGET_DIR=/opt/mq/rabbitmq SBIN_DIR=/opt/mq/rabbitmq/sbin MAN_DIR=/opt/mq/rabbitmq/man
```
开启 web 插件
```
cd /opt/mq/rabbitmq/sbin 
mkdir /etc/rabbitmq/ 
./rabbitmq-plugins enable rabbitmq_management
```

# 启动和关闭RabbitMQ

```
启动监控管理器: rabbitmq-plugins enable rabbitmq_management
关闭监控管理器: rabbitmq-plugins disable rabbitmq_management
启动rabbitmq: rabbitmq-service start
关闭rabbitmq: rabbitmq-service stop
查看所有的队列: rabbitmqctl list_queues
清除所有的队列: rabbitmqctl reset
关闭应用: rabbitmqctl stop_app
启动应用: rabbitmqctl start_app
```
管理界面
```
ip:15672
```
默认用户名和密码都是 guest

