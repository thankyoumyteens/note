# 源码安装

```
wget http://www.keepalived.org/software/keepalived-2.0.7.tar.gz
tar xvf keepalived-2.0.7.tar.gz
cd keepalived-2.0.7
./configure --prefix=/usr/local/keepalived
make && make install
```

# 将配置文件拷贝到系统对应的目录下

keepalived启动时会从/etc/keepalived目录下查找keepalived.conf配置文件，如果没有找到则使用默认的配置。/etc/keepalived目录安装时默认是没有安装的，需要手动创建。

```bash
mkdir /etc/keepalived
cp /usr/local/keepalived/etc/keepalived.conf /etc/keepalived/keepalived.conf
cp /usr/local/keepalived/etc/rc.d/init.d/keepalived /etc/rc.d/init.d/keepalived
cp /usr/local/keepalived/etc/sysconfig/keepalived /etc/sysconfig/keepalived
```

```bash
chkconfig keepalived on
service keepalived start   #启动服务
service keepalived stop    #停止服务
service keepalived restart #重启服务
```
