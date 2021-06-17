# Ubuntu安装Nginx

安装
```
sudo apt-get update
sudo apt-get install nginx
```
nginx文件安装完成之后的文件位置：

- `/usr/sbin/nginx`：主程序
- `/etc/nginx`：存放配置文件
- `/usr/share/nginx`：存放静态文件
- `/var/log/nginx`：存放日志

# CentOS安装Nginx

添加 yum 源
```
sudo rpm -ivh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm
```
yum 安装 Nginx
```
sudo yum install nginx
```
设置开机启动
```
sudo systemctl enable nginx
```
打开防火墙端口
```
sudo firewall-cmd --zone=public --permanent --add-service=http
sudo firewall-cmd --reload
```

# 源码安装

安装依赖包
```
apt-get install gcc
apt-get install libpcre3 libpcre3-dev
apt-get install zlib1g zlib1g-dev
# Ubuntu14.04的仓库中没有发现openssl-dev，由libssl-dev替代
# apt-get install openssl openssl-dev
sudo apt-get install openssl 
sudo apt-get install libssl-dev
```
安装nginx
```
cd /usr/local
mkdir nginx
cd nginx
wget http://nginx.org/download/nginx-1.13.7.tar.gz
tar -xvf nginx-1.13.7.tar.gz 
```
编译
```
# 进入nginx目录
/usr/local/nginx/nginx-1.13.7
# 执行命令
./configure
# 执行make命令
make
# 执行make install命令
make install
```
启动nginx
```
#进入nginx启动目录
cd /usr/local/nginx/sbin
# 启动nginx
./nginx
```
