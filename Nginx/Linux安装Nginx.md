# Ubuntu安装Nginx

安装
```
sudo apt-get update
sudo apt-get install nginx
```

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
