# 查询用户

```sql
-- user: 用户名
-- host: 白名单
-- authentication_string: 密码
-- plugin: 加密插件
select user, host, authentication_string, plugin from mysql.user;
```

输出:

```
+-------------+-----------+-------------------------------------------+-----------------------+
| User        | Host      | authentication_string                     | plugin                |
+-------------+-----------+-------------------------------------------+-----------------------+
| mariadb.sys | localhost |                                           | mysql_native_password |
| root        | localhost | *6BB4837EB74329105CC4568DDA7AB67ED2CA2AD9 | mysql_native_password |
| mysql       | localhost | invalid                                   | mysql_native_password |
| test        | %         | *6BB4837EB74329105CC4568DDA7AB67ED2CA2AD9 | mysql_native_password |
+-------------+-----------+-------------------------------------------+-----------------------+
```
