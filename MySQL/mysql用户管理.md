# 管理用户

添加用户
```sql
CREATE USER '用户名'@'主机名' IDENTIFIED BY '密码';
```
删除用户
```sql
DROP USER '用户名'@'主机名';
```
修改用户密码
```sql
UPDATE USER SET PASSWORD=PASSWORD('新密码') WHERE USER='用户名';
SET PASSWORD FOR '用户名'@'主机名'=PASSWORD('新密码');
```
查询用户
```sql
USE myql;
SELECT * FROM USER;
```

# 权限管理

查询权限
```sql
SHOW GRANTS FOR '用户名'@'主机名';
SHOW GRANTS FOR 'lisi'@'%';
```
授予权限
```sql
grant 权限列表 on 数据库名.表名 to '用户名'@'主机名';
GRANT ALL ON *.* TO 'zhangsan'@'localhost';
```
撤销权限
```sql
revoke 权限列表 on 数据库名.表名 from '用户名'@'主机名';
REVOKE UPDATE ON db3.account FROM 'lisi'@'%';
```
