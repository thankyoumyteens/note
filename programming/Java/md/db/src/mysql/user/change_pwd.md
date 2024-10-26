# 修改密码

```sql
alter user 用户名@'白名单' identified by '密码';

-- 指定密码的加密插件为mysql_native_password, 用来兼容老版本客户端
alter user 用户名@'白名单' identified with mysql_native_password by '密码';
```
