# 安装 mariadb

1. 安装

```sh
sudo apt update
sudo apt-get install -y mariadb-server
```

2. 查看运行状态

```sh
sudo systemctl status mariadb
```

3. 初始化

```sh
sudo mysql_secure_installation

# 因为之前没有设置密码，所以直接回车
Enter current password for root (enter for none):
# 不使用
Switch to unix_socket authentication [Y/n] n
# 设置root密码
Change the root password? [Y/n] y
# 移除匿名用户
Remove anonymous users? [Y/n] y
# 禁止远程登录root
Disallow root login remotely? [Y/n] y
# 删除测试数据库
Remove test database and access to it? [Y/n] y
# 刷新权限
Reload privilege tables now? [Y/n] y
```

4. 以 root 身份登录

```sh
sudo mysql -u root -p
```

5. 创建用户

```sql
-- 创建数据库
create database `db_test`;
-- 创建用户
create user '用户名'@'%' identified by '密码';
-- 授权
grant SELECT, INSERT, UPDATE, REFERENCES, DELETE, CREATE, DROP, ALTER, INDEX, CREATE VIEW, SHOW VIEW on `db_test`.* to '用户名'@'%';
-- 刷新权限
flush privileges;
```

6. 允许远程连接

```sh
vim /etc/mysql/mariadb.conf.d/50-server.cnf

# 在 [mysqld] 下添加:
# bind-address = 0.0.0.0
# 如果 bind-address 已经存在
# 就把它的值修改成0.0.0.0

sudo systemctl restart mariadb
```
