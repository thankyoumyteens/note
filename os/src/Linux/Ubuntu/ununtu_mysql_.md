# ununtu 安装 mysql

1. 去[https://downloads.mysql.com/archives/community/](https://downloads.mysql.com/archives/community/)下载合适的版本, 下载 tar 包。

2. 解压

3. 安装

```sh
sudo apt-get install ./libmysql*
sudo apt-get install libtinfo5

sudo apt-get install ./mysql-community-client_5.7.20-1ubuntu16.04_amd64.deb
# 如果报错就执行一遍这个, 后面也是
# sudo chmod 777 ./mysql-community-client_5.7.20-1ubuntu16.04_amd64.deb
sudo apt-get install ./mysql-client_5.7.20-1ubuntu16.04_amd64.deb
sudo apt-get install ./mysql-community-server_5.7.20-1ubuntu16.04_amd64.deb
sudo apt-get install ./mysql-server_5.7.20-1ubuntu16.04_amd64.deb
```

4. 查看 mysql 状态

```sh
sudo systemctl status mysql
```

5. 登陆

```sh
mysql -u root -p
```

## 重置 root 密码

1. 修改配置文件 `/etc/mysql/mysql.conf.d/mysqld.cnf`

```conf
[mysqld]
skip-grant-tables
```

2. 重启 mysql

```sh
sudo systemctl restart mysql
```

3. 空密码登陆 mysql

```sh
mysql -u root -p
# 密码不用输直接回车
```

4. 修改密码

```sh
use mysql
update user set authentication_string=PASSWORD("密码") where User='root';
update user set plugin="mysql_native_password";
flush privileges;
```

5. 重启 mysql

```sh
sudo systemctl restart mysql
```

## 添加用户

```sh
use mysql
CREATE USER '用户名'@'%' IDENTIFIED BY '密码';
GRANT ALL ON *.* TO '用户名'@'%';
flush privileges;
```

## 远程无法连接

1. 进入云服务器控制台, 修改安全组, 将数据库端口加一下(默认为 3306), 然后继续尝试连接

2. 依旧连不上, 还是一样被拒绝, 查一下 3306 端口的占用情况: 

```sh
$ netstat -an | grep 3306
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      17834/mysqld
```

3. 看到 3306 端口绑定的 IP 是 127.0.0.1, 需要修改配置文件 `/etc/mysql/mysql.conf.d/mysqld.cnf`

```conf
bind-address = 0.0.0.0
```

4. 重启 mysql

```sh
sudo systemctl restart mysql
```

5. 可以连上了, 再查一下 3306 端口的占用情况: 

```sh
$ netstat -an | grep 3306
tcp        0      0 0.0.0.0:3306            0.0.0.0:*               LISTEN      20660/mysqld
```
