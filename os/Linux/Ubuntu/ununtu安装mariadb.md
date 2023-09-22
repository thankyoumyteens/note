# 安装

```sh
sudo apt update
sudo apt install -y mariadb-server
```

# 查看运行状态

```sh
sudo systemctl status mysql
```

# 初始化

```sh
sudo mysql_secure_installation
```

```sh
# 由于没有设置 root 密码，所以这里仅仅输入回车"Enter"即可
Enter current password for root (enter for none):
# 接下来，会提示是否为 MySQL root 用户设置密码
# 在 Ubuntu 上，MariaDB 用户默认使用auth_socket进行鉴权
Set root password? [Y/n] n
# 移除匿名用户
Remove anonymous users? [Y/n] Y
# 限制 root 用户访问本地机器
Disallow root login remotely? [Y/n] Y
# 移除测试数据库
Remove test database and access to it? [Y/n] Y
# 重新加载权限表
Reload privilege tables now? [Y/n] Y
```

# 以 root 身份登录

```sh
sudo mysql
```

# 创建用户

```sh
sudo mysql
CREATE USER '用户名'@'%' IDENTIFIED BY '密码';
GRANT ALL ON *.* TO '用户名'@'%';
flush privileges;
```
