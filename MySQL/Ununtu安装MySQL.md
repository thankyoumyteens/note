# 安装
下载解压
```
wget https://cdn.mysql.com//Downloads/MySQL-5.7/mysql-server_5.7.34-1ubuntu18.04_amd64.deb-bundle.tar
tar -xvf mysql-server_5.7.34-1ubuntu18.04_amd64.deb-bundle.tar
```

预配置MySQL服务器软件包：
```
sudo dpkg-preconfigure mysql-community-server_*.deb
```
对于MySQL服务器的基本安装，请安装数据库公用文件包，客户端包，客户端元包，服务器包和服务器元包（按此顺序）; 可以使用单个命令来执行此操作：
```
sudo dpkg -i mysql-common_*.deb
sudo dpkg -i mysql-community-client_*.deb
sudo dpkg -i mysql-client_*.deb
sudo dpkg -i mysql-community-server_*.deb
sudo dpkg -i mysql-server_*.deb
```
如果中途被dpkg警告未满足的依赖关系 ，可以使用apt-get来修复它们，然后再运行中断的命令
```
sudo apt-get -f install -y
```
通过这种方式安装好之后开机自启动都已经配置好，和命令行上的环境变量，无需手动配置

```
服务启动后端口查询
```
sudo netstat -anp | grep mysql
```
启动
```
sudo service mysql start
```
停止
```
sudo service mysql stop
```
服务状态
```
sudo service mysql status
```
连接数据库
```
mysql -h 127.0.0.1 -P 3306 -uroot -phonglang
```
测试SQL
```
show databases;
```

# 卸载

首先使用以下命令删除MySQL服务器：
```
sudo apt-get remove mysql-server
```
然后，删除随MySQL服务器自动安装的任何其他软件：
```
sudo apt-get autoremove
```
卸载其他组件：
```
sudo apt-get remove <<package-name>>
```
查看从MySQL APT存储库安装的软件包列表：
```
dpkg -l | grep mysql | grep ii
```
